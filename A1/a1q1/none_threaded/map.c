/* map.c
 * ----------------------------------------------------------
 *  CS350
 *  Assignment 1
 *  Question 1
 *
 *  Purpose:  Gain experience with threads and basic 
 *  synchronization.
 *
 *  YOU MAY ADD WHATEVER YOU LIKE TO THIS FILE.
 *  YOU CANNOT CHANGE THE SIGNATURE OF CountOccurrences.
 * ----------------------------------------------------------
 */
#include "data.h"
#include <stdlib.h>

/* --------------------------------------------------------------------
 * CountOccurrences
 * --------------------------------------------------------------------
 * Takes a Library of articles containing words and a word.
 * Returns the total number of times that the word appears in the 
 * Library.
 *
 * For example, "There the thesis sits on the theatre bench.", contains
 * 2 occurences of the word "the".
 * --------------------------------------------------------------------
 */
int TOTAL = 0;

int CountOccurrences( struct  Library * lib, char * word )
{
    for ( unsigned int i = 0; i < lib->numArticles; i ++ ) {
        for ( unsigned int j = 0; j < lib->articles[i]->numWords; j++) {
            if(strcmp(word, lib->articles[i]->words[j]) == 0) {
                TOTAL++;
            }
        }
    }   
    return TOTAL;
}

