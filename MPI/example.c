// mpicc example.c -o mpi_demo && mpiexec -n 4 ./mpi_demo

/*
  "Hello World" MPI Test Program
*/
#include <assert.h>
#include <stdio.h>
#include <string.h>
#include <mpi.h>

#define BUFSIZE 256

int main(int argc, char* argv[])
{
    char buf[BUFSIZE];  /* storage for message */
    int my_rank;        /* rank of process */
    int num_procs;      /* number of processes */
    const int tag = 0;  /* tag for messages */
    MPI_Status status;  /* return status for receive */

    /* start up MPI */
    MPI_Init(&argc, &argv);

    /* find out process rank */
    MPI_Comm_rank(MPI_COMM_WORLD, &my_rank);

    /* find out number of processes */
    MPI_Comm_size(MPI_COMM_WORLD, &num_procs);

    /* Until this point, all programs have been doing exactly the same.
       Here, we check the rank to distinguish the roles of the programs */
    if (my_rank == 0) {
        printf("We have %i processes.\n", num_procs);

        /* Send messages to all other processes */
        for (int dst = 1; dst < num_procs; dst++) {
            sprintf(buf, "Hello %i!", dst);
            MPI_Send(buf, strlen(buf)+1, MPI_CHAR, dst, tag, MPI_COMM_WORLD);
        }

        /* Receive messages from all other processes */
        for (int src = 1; src < num_procs; src++) {
            MPI_Recv(buf, BUFSIZE, MPI_CHAR, src, tag, MPI_COMM_WORLD, &status);
            printf("%s\n", buf);
        }

    } else {

        /* Receive message from process #0 */
        MPI_Recv(buf, BUFSIZE, MPI_CHAR, 0, tag, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        assert(memcmp(buf, "Hello ", 6) == 0);

        /* Send message to process #0 */
        sprintf(buf, "Process %i reporting for duty.", my_rank);
        MPI_Send(buf, strlen(buf)+1, MPI_CHAR, 0, tag, MPI_COMM_WORLD);

    }

    /* shut down MPI */
    MPI_Finalize();
    
    return 0;
}
