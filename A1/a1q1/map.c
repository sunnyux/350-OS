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
#include <math.h>
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
char * WORD = "";
int TOTAL = 0;
int volatile counting;
pthread_mutex_t mut = PTHREAD_MUTEX_INITIALIZER;
pthread_cond_t t_done = PTHREAD_COND_INITIALIZER;

void *Count(void *arg) {
    pthread_mutex_lock(&mut);
    struct Article *art = (struct Article *) arg;
    for ( unsigned int j = 0; j < art->numWords; j++) {
        if(strcmp(WORD, art->words[j]) == 0) {
            TOTAL++;
        }
    }
    counting--;
    while (counting > 0) {
        pthread_cond_wait(&t_done, &mut);
    }
    pthread_cond_signal(&t_done);
    pthread_mutex_unlock(&mut);
    return NULL;
}


int CountOccurrences( struct  Library * lib, char * word )
{
    WORD = word;
    unsigned int numArticles = lib->numArticles;
    counting = numArticles;
    pthread_t thread[numArticles];

    for(int i = 0; i < numArticles; i++) {
        pthread_create(&thread[i], NULL, Count, (void*) lib->articles[i]);
    }

    pthread_mutex_lock(&mut);
    while (counting > 0) {
        pthread_cond_wait(&t_done, &mut);
    }
    pthread_mutex_unlock(&mut);

    return TOTAL;
}

