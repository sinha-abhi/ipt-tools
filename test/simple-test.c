#include <stdio.h>

void print(int x) {
  while (x < 300) {
    if (x > 0)
      x += 2;
    x++;
  }
}

int main() {
  int x = 1;
  if (x < 0)
    printf("ayo\n");
  if (x == 0)
    printf("true\n");
  print(x);
  return 0;
}
