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
char * WORD = "";
int TOTAL = 0;
int volatile counting = 2;
pthread_mutex_t mut = PTHREAD_MUTEX_INITIALIZER;
pthread_cond_t t_done = PTHREAD_COND_INITIALIZER;

void *Count(void *arg) {
    pthread_mutex_lock(&mut);
    struct Library *lib = (struct Library *)arg;
    for ( unsigned int i = 0; i < lib->numArticles; i ++ ) {
        for ( unsigned int j = 0; j < lib->articles[i]->numWords; j++) {
            if(strcmp(WORD, lib->articles[i]->words[j]) == 0) {
                TOTAL++;
            }
        }
        printf("\n");
    }
    counting--;
    while (counting > 0) {
        pthread_cond_wait(&t_done, &mut);
    }
    pthread_cond_signal(&t_done);
    pthread_mutex_unlock(&mut);
}


int CountOccurrences( struct  Library * lib, char * word )
{
    pthread_t thread1, thread2;
    WORD = word;
    unsigned int numArticles = lib->numArticles;

    struct Library * lib1 = ( struct Library * )malloc( sizeof( struct Library ) );
    struct Library * lib2 = ( struct Library * )malloc( sizeof( struct Library ) );
    lib1->articles = ( struct Article ** )malloc( numArticles/2 * sizeof( struct Article * ) );
    lib2->articles = ( struct Article ** )malloc( numArticles/2 * sizeof( struct Article * ) );
    lib1->numArticles = numArticles/2;
    lib2->numArticles = numArticles/2;

    for ( unsigned int i = 0; i < numArticles/2; i++ ) {
        lib1->articles[i] = lib->articles[i];
    }

    for ( unsigned int i = numArticles/2; i < numArticles; i++ ) {
        lib2->articles[i - numArticles/2] = lib->articles[i];
    }

    pthread_create(&thread1, NULL, Count, lib1);
    pthread_create(&thread2, NULL, Count, lib2);

    pthread_mutex_lock(&mut);
    while (counting > 0) {
        pthread_cond_wait(&t_done, &mut);
    }
    pthread_mutex_unlock(&mut);

    return TOTAL;
}

