#include <stdio.h>
int main() {
  int x = 0;
  for ( ; ; ) {
    if (x < 20) 
      x++;
    else 
      break;
  }
  return 0;
}
