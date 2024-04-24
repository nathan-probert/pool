// standard libraries
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <math.h>

// header file
#include "phylib.h"

// create new still ball
phylib_object *phylib_new_still_ball( unsigned char number, phylib_coord *pos ) {
    phylib_object *object = malloc(sizeof(phylib_object));

    // return null if malloc fails
    if (object == NULL) {
        return NULL;
    }
    object->type = PHYLIB_STILL_BALL;

    // set attributes
    object->obj.still_ball.number = number;
    object->obj.still_ball.pos = *pos;

    return object;
}

// create new rolling ball
phylib_object *phylib_new_rolling_ball( unsigned char number, phylib_coord *pos, phylib_coord *vel, phylib_coord *acc ) {
    phylib_object *object = malloc(sizeof(phylib_object));

    // return null if malloc fails
    if (object == NULL) {
        return NULL;
    }
    object->type = PHYLIB_ROLLING_BALL;

    // set attributes
    object->obj.rolling_ball.number = number;
    object->obj.rolling_ball.pos = *pos;
    object->obj.rolling_ball.vel = *vel;
    object->obj.rolling_ball.acc = *acc;

    return object;
}

phylib_object *phylib_new_hole( phylib_coord *pos ) {
    phylib_object *object = malloc(sizeof(phylib_object));

    // return null if malloc fails
    if (object == NULL) {
        return NULL;
    }
    object->type = PHYLIB_HOLE;
    
    // set attributes
    object->obj.hole.pos = *pos;

    return object;
}

phylib_object *phylib_new_hcushion( double y ) {
    phylib_object *object = malloc(sizeof(phylib_object));

    // return null if malloc fails
    if (object == NULL) {
        return NULL;
    }
    object->type = PHYLIB_HCUSHION;
    
    // set attributes
    object->obj.hcushion.y = y;

    return object;
}

phylib_object *phylib_new_vcushion( double x ) {
    phylib_object *object = malloc(sizeof(phylib_object));

    // return null if malloc fails
    if (object == NULL) {
        return NULL;
    }
    object->type = PHYLIB_VCUSHION;
    
    // set attributes
    object->obj.vcushion.x = x;

    return object;
}

phylib_table *phylib_new_table( void ) {
    phylib_table *table = malloc(sizeof(phylib_table));

    // return null if malloc fails
    if (table == NULL) {
        return NULL;
    }

    // set inital time to 0
    table->time = 0.0;

    // add horizontal cushions to table
    table->object[0] = phylib_new_hcushion(0.0);
    table->object[1] = phylib_new_hcushion(PHYLIB_TABLE_LENGTH);

    // add vertical cushions to table
    table->object[2] = phylib_new_vcushion(0.0);
    table->object[3] = phylib_new_vcushion(PHYLIB_TABLE_WIDTH);

    // add the 6 holes to the table
    phylib_coord top_left_corner = {0.0, 0.0};
    table->object[4] = phylib_new_hole(&top_left_corner);

    phylib_coord middle_left_corner = {0.0, PHYLIB_TABLE_LENGTH/2};
    table->object[5] = phylib_new_hole(&middle_left_corner);

    phylib_coord bottom_left_corner = {0.0, PHYLIB_TABLE_LENGTH};
    table->object[6] = phylib_new_hole(&bottom_left_corner);

    phylib_coord top_right_corner = {PHYLIB_TABLE_WIDTH, 0.0};
    table->object[7] = phylib_new_hole(&top_right_corner);  

    phylib_coord middle_right_corner = {PHYLIB_TABLE_WIDTH, PHYLIB_TABLE_LENGTH/2};
    table->object[8] = phylib_new_hole(&middle_right_corner);

    phylib_coord bottom_right_corner = {PHYLIB_TABLE_WIDTH, PHYLIB_TABLE_LENGTH};
    table->object[9] = phylib_new_hole(&bottom_right_corner);

    // set remaining objects to null
    for (int i=10; i<PHYLIB_MAX_OBJECTS; i++) {
        table->object[i] = NULL;
    }

    return table;
}

// utility functions

// copy object
void phylib_copy_object( phylib_object **dest, phylib_object **src ) {
    // set destination to null if source is null
    if (*src == NULL) {
        *dest = NULL;
    } else {
        // allocate memory for dest then copy
        *dest = malloc(sizeof(phylib_object));

        // check malloc
        if (*dest != NULL) {
            memcpy(*dest, *src, sizeof(phylib_object));
        }
    }
}

// copy table
phylib_table *phylib_copy_table( phylib_table *table ) {
    phylib_table *newTable = malloc(sizeof(phylib_table));

    // return null if malloc fails
    if (newTable == NULL) {
        return NULL;
    }

    // copy time and base of array
    memcpy(newTable, table, sizeof(phylib_table));

    // copy all objects in array
    for (int i=0; i<PHYLIB_MAX_OBJECTS; i++) {
        phylib_copy_object(&(newTable->object[i]), &(table->object[i]));
    }

    return newTable;
}

// add object to a table
void phylib_add_object( phylib_table *table, phylib_object *object ) {
    // find a null pointer (or exceed the array)
    int i=0; 
    while ((i<PHYLIB_MAX_OBJECTS) && (table->object[i] != NULL)) {
        i++;
    }

    // if within the range of the array, set the object
    if ((i < PHYLIB_MAX_OBJECTS) && (table->object[i] == NULL)) {
        table->object[i] = object;
    }
}

// free the table
void phylib_free_table( phylib_table *table ) {
    // free all objects
    for (int i=0; i<PHYLIB_MAX_OBJECTS; i++) {
        if (table->object[i] != NULL) {
            free(table->object[i]);
        }
    }

    // free the table itself
    free(table);
}

// subtract two vectors
phylib_coord phylib_sub( phylib_coord c1, phylib_coord c2 ) {
    // new x = c1.x - c2.x
    // new y = c1.y - c2.y

    // variable to return
    phylib_coord coord = c1;
    coord.x -= c2.x;
    coord.y -= c2.y;

    return coord;
}

// get length of a vector
double phylib_length( phylib_coord c ) {
    return sqrt(c.x * c.x + c.y * c.y);
}

// dot product of a vector
double phylib_dot_product( phylib_coord a, phylib_coord b ) {
    return (a.x * b.x + a.y * b.y);
}

// get distance between two objects
double phylib_distance( phylib_object *obj1, phylib_object *obj2 ) {
    // check if obj1 is rolling ball
    if (obj1->type != PHYLIB_ROLLING_BALL) {
        return -1.0;
    }

    // set return value
    double final = -1.0;

    // set "shortcuts"
    double obj1X = (obj1->obj.rolling_ball.pos.x);
    double obj1Y = (obj1->obj.rolling_ball.pos.y);

    if (obj2->type == PHYLIB_STILL_BALL || obj2->type == PHYLIB_ROLLING_BALL) {
        // case 1 : obj2 is a ball
        
        // compute distance between center of two balls then subtract the 2 radii

        // distance formula : d = root( (x2 - x1)^2 + (y2 - y1)^2 )

        double obj2X = (obj2->obj.rolling_ball.pos.x);
        double obj2Y = (obj2->obj.rolling_ball.pos.y);

        final = sqrt( (obj2X - obj1X)*(obj2X - obj1X) + (obj2Y - obj1Y)*(obj2Y - obj1Y) );
        final -= PHYLIB_BALL_DIAMETER;

    } else if (obj2->type == PHYLIB_HOLE) {
        // case 2 : obj2 is a hole

        double obj2X = (obj2->obj.hole.pos.x);
        double obj2Y = (obj2->obj.hole.pos.y);

        final = sqrt( (obj2X - obj1X)*(obj2X - obj1X) + (obj2Y - obj1Y)*(obj2Y - obj1Y) );
        final -= PHYLIB_HOLE_RADIUS;

    } else if (obj2->type == PHYLIB_HCUSHION) {
        // case 3 : obj2 is a cushion

        double obj2X = obj1X;
        double obj2Y = (obj2->obj.hcushion.y);

        final = fabs((sqrt( (obj2X - obj1X)*(obj2X - obj1X) + (obj2Y - obj1Y)*(obj2Y - obj1Y) )));
        final -= PHYLIB_BALL_RADIUS;

    } else if (obj2->type == PHYLIB_VCUSHION) {
        // case 3 : obj2 is a cushion

        double obj2X = (obj2->obj.vcushion.x);
        double obj2Y = obj1Y;

        final = fabs(sqrt( (obj2X - obj1X)*(obj2X - obj1X) + (obj2Y - obj1Y)*(obj2Y - obj1Y) ));
        final -= PHYLIB_BALL_RADIUS;

    }

    // returns -1 if obj2 isnt valid type (final will be equal to -1)
    return final;
}

// get distance between two objects
double phylib_new_distance( phylib_object *obj1, phylib_object *obj2 ) {
    // check if obj1 is rolling ball
    if (obj1->type != PHYLIB_ROLLING_BALL) {
        return -1.0;
    }

    // set return value
    double final = -1.0;

    // set "shortcuts"
    double obj1X = (obj1->obj.rolling_ball.pos.x);
    double obj1Y = (obj1->obj.rolling_ball.pos.y);

    if (obj2->type == PHYLIB_STILL_BALL || obj2->type == PHYLIB_ROLLING_BALL) {
        // case 1 : obj2 is a ball
        
        // compute distance between center of two balls then subtract the 2 radii

        // distance formula : d = root( (x2 - x1)^2 + (y2 - y1)^2 )

        double obj2X = (obj2->obj.rolling_ball.pos.x);
        double obj2Y = (obj2->obj.rolling_ball.pos.y);

        final = ( (obj2X - obj1X)*(obj2X - obj1X) + (obj2Y - obj1Y)*(obj2Y - obj1Y) );
        final -= PHYLIB_BALL_DIAMETER*PHYLIB_BALL_DIAMETER;

    } else if (obj2->type == PHYLIB_HOLE) {
        // case 2 : obj2 is a hole

        double obj2X = (obj2->obj.hole.pos.x);
        double obj2Y = (obj2->obj.hole.pos.y);

        final = ( (obj2X - obj1X)*(obj2X - obj1X) + (obj2Y - obj1Y)*(obj2Y - obj1Y) );
        final -= PHYLIB_HOLE_RADIUS*PHYLIB_HOLE_RADIUS;

    } else if (obj2->type == PHYLIB_HCUSHION) {
        // case 3 : obj2 is a cushion

        double obj2X = obj1X;
        double obj2Y = (obj2->obj.hcushion.y);

        final = fabs((( (obj2X - obj1X)*(obj2X - obj1X) + (obj2Y - obj1Y)*(obj2Y - obj1Y) )));
        final -= PHYLIB_BALL_RADIUS*PHYLIB_BALL_RADIUS;

    } else if (obj2->type == PHYLIB_VCUSHION) {
        // case 3 : obj2 is a cushion

        double obj2X = (obj2->obj.vcushion.x);
        double obj2Y = obj1Y;

        final = fabs(( (obj2X - obj1X)*(obj2X - obj1X) + (obj2Y - obj1Y)*(obj2Y - obj1Y) ));
        final -= PHYLIB_BALL_RADIUS*PHYLIB_BALL_RADIUS;
    }

    // returns -1 if obj2 isnt valid type (final will be equal to -1)
    return final;
}

// pt 3

// roll an object for given amount of time
void phylib_roll( phylib_object *new, phylib_object *old, double time ) {
    // only do anything if object is a rolling ball
    if (new->type == PHYLIB_ROLLING_BALL && old->type == PHYLIB_ROLLING_BALL) {

        // set shortcut for old ball
        phylib_rolling_ball oldBall = old->obj.rolling_ball;

        // update position
        new->obj.rolling_ball.pos.x = oldBall.pos.x + oldBall.vel.x * time + 0.5 * oldBall.acc.x * time * time;
        new->obj.rolling_ball.pos.y = oldBall.pos.y + oldBall.vel.y * time + 0.5 * oldBall.acc.y * time * time;
    
        // update velocity
        new->obj.rolling_ball.vel.x = oldBall.vel.x + oldBall.acc.x * time;
        new->obj.rolling_ball.vel.y = oldBall.vel.y + oldBall.acc.y * time;

        // if velocity switched (ball reversed), stop ball
        if (oldBall.vel.x > 0 && new->obj.rolling_ball.vel.x < 0) {
            new->obj.rolling_ball.vel.x = 0;
            new->obj.rolling_ball.acc.x = 0;
        }

        // if velocity switched (ball reversed), stop ball
        if (oldBall.vel.y > 0 && new->obj.rolling_ball.vel.y < 0) {
            new->obj.rolling_ball.vel.y = 0;
            new->obj.rolling_ball.acc.y = 0;
        }

        // if velocity switched (ball reversed), stop ball
        if (oldBall.vel.x < 0 && new->obj.rolling_ball.vel.x > 0) {
            new->obj.rolling_ball.vel.x = 0;
            new->obj.rolling_ball.acc.x = 0;
        }

        // if velocity switched (ball reversed), stop ball
        if (oldBall.vel.y < 0 && new->obj.rolling_ball.vel.y > 0) {
            new->obj.rolling_ball.vel.y = 0;
            new->obj.rolling_ball.acc.y = 0;
        }
    }
}

// check if rolling ball stopped
unsigned char phylib_stopped( phylib_object *object ) {
    // can assume object is rolling ball

    if (phylib_length(object->obj.rolling_ball.vel) < PHYLIB_VEL_EPSILON) {
        // convert to still ball by changing type to still ball
        object->type = PHYLIB_STILL_BALL;

        return 1;
    }

    return 0;
}

// handle collisions
void phylib_bounce( phylib_object **a, phylib_object **b ) {
    // assume a is rolling ball

    switch ((*b)->type) {

        case PHYLIB_HCUSHION:
        {
            // case 1 : b is a horizonal cushion

            // y = y not
            (*a)->obj.rolling_ball.vel.y *= -1;
            (*a)->obj.rolling_ball.acc.y *= -1;
            
            break;
        }

        case PHYLIB_VCUSHION:
        {
            // case 2 : b is a vertical cushion

            // x = x not
            (*a)->obj.rolling_ball.vel.x *= -1;
            (*a)->obj.rolling_ball.acc.x *= -1;

            break;
        }

        case PHYLIB_HOLE:
        {
            // case 3 : b is a hole

            // free a (ball) and set to null (ball in hole now)
            free(*a);
            *a = NULL;

            break;
        }

        case PHYLIB_STILL_BALL:
            // case 4 : b is a still ball

            // upgrade b to rolling ball
            (*b)->type = PHYLIB_ROLLING_BALL;
            (*b)->obj.rolling_ball.vel.x = 0.0;
            (*b)->obj.rolling_ball.vel.y = 0.0;
            (*b)->obj.rolling_ball.acc.x = 0.0;
            (*b)->obj.rolling_ball.acc.y = 0.0;
            
            // proceed to case 5 (no break statement)
            // FALLTHROUGH

        case PHYLIB_ROLLING_BALL:
        {
            // case 5 : b is a rolling ball

            // get relative position and velocity
            phylib_coord r_ab = phylib_sub( (*a)->obj.rolling_ball.pos , (*b)->obj.rolling_ball.pos );
            phylib_coord v_rel = phylib_sub( (*b)->obj.rolling_ball.vel , (*a)->obj.rolling_ball.vel );

            // get normal vector
            double len_r_ab = phylib_length(r_ab);
            phylib_coord n = {r_ab.x / len_r_ab, r_ab.y / len_r_ab};

            // get ratio of relative velocity
            double v_rel_n = phylib_dot_product(v_rel, n);

            // update positions
            (*a)->obj.rolling_ball.vel.x += v_rel_n * n.x;
            (*a)->obj.rolling_ball.vel.y += v_rel_n * n.y;
            (*b)->obj.rolling_ball.vel.x -= v_rel_n * n.x;
            (*b)->obj.rolling_ball.vel.y -= v_rel_n * n.y;

            // update velocities
            double aLen = phylib_length((*a)->obj.rolling_ball.vel);
            if (aLen > PHYLIB_VEL_EPSILON) {
                (*a)->obj.rolling_ball.acc.x = -((*a)->obj.rolling_ball.vel.x / aLen) * PHYLIB_DRAG;
                (*a)->obj.rolling_ball.acc.y = -((*a)->obj.rolling_ball.vel.y / aLen) * PHYLIB_DRAG;
            }
            double bLen = phylib_length((*b)->obj.rolling_ball.vel); 
            if (bLen > PHYLIB_VEL_EPSILON) {
                (*b)->obj.rolling_ball.acc.x = -((*b)->obj.rolling_ball.vel.x / bLen) * PHYLIB_DRAG;
                (*b)->obj.rolling_ball.acc.y = -((*b)->obj.rolling_ball.vel.y / bLen) * PHYLIB_DRAG;
            }

            break;
        }
        
    }
}

// count number of rolling balls
unsigned char phylib_rolling( phylib_table *t ) {
    // init count variable
    unsigned char count = 0;

    // for each object, check if type is rolling ball
    for (int i=0; i<PHYLIB_MAX_OBJECTS; i++) {
        if (t->object[i] != NULL && t->object[i]->type == PHYLIB_ROLLING_BALL) {
            count++;
        }
    }

    return count;
}

// return segment of a pool shot
phylib_table *phylib_segment( phylib_table *table ) {
    // return null if no balls are rolling
    int rollingBalls = phylib_rolling(table);
    if (rollingBalls == 0) {
        return NULL;
    }

    // create copy of the table
    phylib_table* newTable = phylib_copy_table(table);

    // loop over time to avoid infinite loop
    for (double time = PHYLIB_SIM_RATE; time < PHYLIB_MAX_TIME; time += PHYLIB_SIM_RATE) { 
        newTable->time += PHYLIB_SIM_RATE;  
        // iterate through each object
        for (int i=0; i<PHYLIB_MAX_OBJECTS; i++) {
            // check if object is a rolling ball
            if (table->object[i] != NULL && table->object[i]->type == PHYLIB_ROLLING_BALL) {
                // roll the ball and increment time
                phylib_roll(newTable->object[i], table->object[i], time);
                
                // if ball stopped, return
                if (phylib_stopped(newTable->object[i])) {
                    return newTable;
                }
            }
        }

        // check for collisions
        for (int i=10 ; i<PHYLIB_MAX_OBJECTS; i++) {
            if (table->object[i] != NULL && table->object[i]->type == PHYLIB_ROLLING_BALL) {
                for (int j=0; j<PHYLIB_MAX_OBJECTS; j++) {
                    if (j != i && newTable->object[j] != NULL) {
                        // get distance
                        if (phylib_new_distance(newTable->object[i], newTable->object[j]) < 0.0) {
                            // if objects are hitting each other, bounce
                            phylib_bounce(&newTable->object[i], &newTable->object[j]);
                            return newTable;
                        }
                    }
                }
            }
        }
    }

    return NULL;
}

char *phylib_object_string( phylib_object *object )
{
    static char string[80];
    if (object==NULL)
    {
        sprintf( string, "NULL;" );
        return string;
    }

    switch (object->type)
    {
        case PHYLIB_STILL_BALL:
        sprintf( string,
            "STILL_BALL (%d,%6.1lf,%6.1lf)",
            object->obj.still_ball.number,
            object->obj.still_ball.pos.x,
            object->obj.still_ball.pos.y );
        break;

        case PHYLIB_ROLLING_BALL:
        sprintf( string,
            "ROLLING_BALL (%d,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf)",
            object->obj.rolling_ball.number,
            object->obj.rolling_ball.pos.x,
            object->obj.rolling_ball.pos.y,
            object->obj.rolling_ball.vel.x,
            object->obj.rolling_ball.vel.y,
            object->obj.rolling_ball.acc.x,
            object->obj.rolling_ball.acc.y );
        break;

        case PHYLIB_HOLE:
        sprintf( string,
            "HOLE (%6.1lf,%6.1lf)",
            object->obj.hole.pos.x,
            object->obj.hole.pos.y );
        break;

        case PHYLIB_HCUSHION:
        sprintf( string,
            "HCUSHION (%6.1lf)",
            object->obj.hcushion.y );
        break;

        case PHYLIB_VCUSHION:
        sprintf( string,
            "VCUSHION (%6.1lf)",
            object->obj.vcushion.x );
        break;
    }

    return string;
}
