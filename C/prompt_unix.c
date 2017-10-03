#include <stdio.h>
#include <stdlib.h>

#include <editline/readline.h>

int main(int argc, char** argv) {
   
  /* Print Version and Exit Information */
  puts("SCLI Version 0.4-alpha");
  puts("Press Ctrl+C to Exit\n");
   
  /* In a never ending loop */
  while (1) {
    
    /* Output our prompt and get input */
    char* input = readline("scli v0.4-alpha > ");
    
    /* Add input to history */
    add_history(input);
    
    /* Echo input back to user */    
    printf("You somehow broke me");

    /* Free retrived input */
    free(input);
    
  }
  
  return 0;
}
