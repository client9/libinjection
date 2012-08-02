/* vi: set ft=c expandtab shiftwidth=4 tabstop=4: */
#ifndef MODP_STDINT_H_
#define MODP_STDINT_H_

#ifndef _WIN32
#  include <stdint.h>
#else
/* win64 is llp64 so these are the same for 32/64bit
   so no check for _WIN64 is required.
 */
  typedef unsigned char uint8_t;
  typedef signed char int8_t;
  typedef unsigned short uint16_t;
  typedef signed short int16_t;
  typedef unsigned int uint32_t;
  typedef signed int int32_t;
  typedef unsigned __int64 uint64_t;
  typedef signed __int64 int64_t;
#endif

#endif /* MODP_STDINT_H_ */
