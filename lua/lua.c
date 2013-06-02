#include <stdio.h>
#include "lua.h"
#include "lualib.h"
#include "lauxlib.h"

extern int luaopen_libinjection(lua_State* L); // declare the wrapped module

int main(int argc,char* argv[])
{
    lua_State *L;
    int result;

    if (argc<2)
    {
        printf("%s: <filename.lua>\n",argv[0]);
        return 0;
    }

    L = luaL_newstate();          /* create state */
    lua_gc(L, LUA_GCSTOP, 0);     /* stop collector during initialization */
    luaL_openlibs(L);             /* open libraries */
    luaopen_libinjection(L);      /*  add swig libinjection */
    lua_gc(L, LUA_GCRESTART, -1); /* restart collector */

    if (luaL_loadfile(L,argv[1])==0) {// load and run the file
        lua_pcall(L,0,0,0);
        result = lua_toboolean(L, -1);  /* get result */
    } else {
        fprintf(stderr, "unable to load %s\n",argv[1]);
        result =1;
    }
    lua_close(L);

    /* flip exit codes true (1) = ok */
    return result ? 0 : 1;
}
