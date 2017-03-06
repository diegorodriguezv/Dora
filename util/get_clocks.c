/*
   gcc -o get_clocks get_clocks.c
   sudo ./get_clocks
*/

/*
get_clocks.c
2016-06-17
Public Domain
*/

#include <stdio.h>
#include <stdlib.h>
#include <stdarg.h>
#include <unistd.h>
#include <stdint.h>
#include <string.h>
#include <fcntl.h>
#include <errno.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <sys/types.h>

static volatile uint32_t piModel = 1;

static volatile uint32_t piPeriphBase = 0x20000000;
static volatile uint32_t piBusAddr = 0x40000000;

#define CLK_BASE   (piPeriphBase + 0x101000)

#define CLK_LEN   0xA8

#define CLK_PASSWD  (0x5A<<24)

#define CLK_CTL_MASH(x)((x)<<9)
#define CLK_CTL_BUSY    (1 <<7)
#define CLK_CTL_KILL    (1 <<5)
#define CLK_CTL_ENAB    (1 <<4)
#define CLK_CTL_SRC(x) ((x)<<0)

#define CLK_CTL_SRC_OSC  1  /* 19.2 MHz */
#define CLK_CTL_SRC_PLLC 5  /* 1000 MHz */
#define CLK_CTL_SRC_PLLD 6  /*  500 MHz */
#define CLK_CTL_SRC_HDMI 7  /*  216 MHz */

#define CLK_GP0_CTL 28
#define CLK_GP1_CTL 30
#define CLK_GP2_CTL 32
#define CLK_PCM_CTL 38
#define CLK_PWM_CTL 40

typedef struct
{
   char *name;
   int base;
} clock_info_t;

clock_info_t clock_info[]=
{
   {"GP0", CLK_GP0_CTL},
   {"GP1", CLK_GP1_CTL},
   {"GP2", CLK_GP2_CTL},
   {"PCM", CLK_PCM_CTL},
   {"PWM", CLK_PWM_CTL},
};

/*

Clock sources

0     0 Hz     Ground
1     19.2 MHz oscillator 
2     0 Hz     testdebug0
3     0 Hz     testdebug1
4     0 Hz     PLLA
5     1000 MHz PLLC (changes with overclock settings)
6     500 MHz  PLLD
7     216 MHz  HDMI auxiliary
8-15  0 Hz     Ground
*/

int src_freq[]=
{
   0, 19200000, 500000000, 0, 0, 1000000000, 500000000, 216000000,
   0,        0,         0, 0, 0,          0,         0,         0
};

static volatile uint32_t  *clkReg  = MAP_FAILED;

unsigned hardwareRevision(void)
{
   static unsigned rev = 0;

   FILE * filp;
   char buf[512];
   char term;
   int chars=4; /* number of chars in revision string */

   if (rev) return rev;

   piModel = 0;

   filp = fopen ("/proc/cpuinfo", "r");

   if (filp != NULL)
   {
      while (fgets(buf, sizeof(buf), filp) != NULL)
      {
         if (piModel == 0)
         {
            if (!strncasecmp("model name", buf, 10))
            {
               if (strstr (buf, "ARMv6") != NULL)
               {
                  piModel = 1;
                  chars = 4;
                  piPeriphBase = 0x20000000;
                  piBusAddr = 0x40000000;
               }
               else if (strstr (buf, "ARMv7") != NULL)
               {
                  piModel = 2;
                  chars = 6;
                  piPeriphBase = 0x3F000000;
                  piBusAddr = 0xC0000000;
               }
            }
         }

         if (!strncasecmp("revision", buf, 8))
         {
            if (sscanf(buf+strlen(buf)-(chars+1),
               "%x%c", &rev, &term) == 2)
            {
               if (term != '\n') rev = 0;
            }
         }
      }

      fclose(filp);
   }
   return rev;
}

static int showClock(int clock)
{
   int ctl, div, src, divi, divf;
   double d, freq;
   char * hz;

   ctl = clock_info[clock].base;
   div = clock_info[clock].base+1;

   src = clkReg[ctl]&15;
   divi = (clkReg[div]>>12)&4095;
   divf = clkReg[div]&4095;

   d = divi + (divf / 4096.0);

   if (divi) freq = src_freq[src]/d;
   else      freq = 0;

   if (freq < 1000)         {hz =  "Hz";                 }
   else if (freq < 1000000) {hz = "kHz"; freq /= 1000;   }
   else                     {hz = "MHz"; freq /= 1000000;}


   printf("%s: src=%d divi=%-4d divf=%-4d freq=%-7.3f %s\n",
      clock_info[clock].name, src, divi, divf, freq, hz);
}

/* Map in registers. */

static uint32_t * initMapMem(int fd, uint32_t addr, uint32_t len)
{
    return (uint32_t *) mmap(0, len,
       PROT_READ|PROT_WRITE|PROT_EXEC,
       MAP_SHARED|MAP_LOCKED,
       fd, addr);
}

int initialise(void)
{
   int fd;

   hardwareRevision(); /* sets piModel, needed for peripherals address */

   fd = open("/dev/mem", O_RDWR | O_SYNC) ;

   if (fd < 0)
   {
      fprintf(stderr,
         "This program needs root privileges.  Try using sudo\n");
      return -1;
   }

   clkReg   = initMapMem(fd, CLK_BASE,  CLK_LEN);

   close(fd);

   if (clkReg == MAP_FAILED)
   {
      fprintf(stderr,
         "Bad, mmap failed\n");
      return -1;
   }
   return 0;
}

int main(int argc, char *argv[])
{
   int i;

   if (initialise() < 0)
   {
      fprintf(stderr, "initialise failed\n");
      return 1;
   }

   for (i=0; i<(sizeof(clock_info)/sizeof(clock_info_t)); i++) showClock(i);
}

