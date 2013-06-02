/* libinjection.i SWIG interface file */
%module libinjection
%{
#include "libinjection.h"

static int libinjection_lua_check_fingerprint(sfilter* sf, void* luaptr)
{
    lua_State* L = (lua_State*) luaptr;
#if 1
    int i;
    int top = lua_gettop(L);
    for (i = 1; i <= top; i++) {  /* repeat for each level */
        int t = lua_type(L, i);
        switch (t) {
    
        case LUA_TSTRING:  /* strings */
            printf("%d `%s'\n", i,lua_tostring(L, i));
            break;
    
        case LUA_TBOOLEAN:  /* booleans */
            printf("%d %s\n", i, lua_toboolean(L, i) ? "true" : "false");
            break;
    
        case LUA_TNUMBER:  /* numbers */
            printf("%d %g\n", i, lua_tonumber(L, i));
            break;
    
        default:  /* other values */
            printf("%d, %s\n", i, lua_typename(L, t));
            break;
    
        }
        printf("  ");  /* put a separator */
    }
    printf("\n");  /* end the listing */

#endif
    char* luafunc = (char *)lua_tostring(L, 4);
    printf("GOT: %s\n", luafunc);
    lua_getglobal(L, (char*) luafunc);
    SWIG_NewPointerObj(L, (void*)sf, SWIGTYPE_p_sfilter, 0);
    if (lua_pcall(L, 1, 1, 0)) {
        printf("Something bad happened");
    }
    int issqli = lua_tonumber(L, -1);
    printf("GOT VALUE: %d\n", issqli);
    return issqli;
}
%}
%include "typemaps.i"

%typemap(in) (ptr_fingerprints_fn fn, void* callbackarg) {
    if (lua_isnil(L, 4)) {
        arg4 = NULL;
        arg5 = NULL;
    } else {
        arg4 = libinjection_lua_check_fingerprint;
        arg5 = (void *) L;
    }
 }


%typemap(out) stoken_t [ANY] {
    printf("Building tokenvec\n");
    int i;
    lua_newtable(L);
    for (i = 0; i < $1_dim0; i++) {
        lua_pushnumber(L, i+1);
        SWIG_NewPointerObj(L, (void*)(& $1[i]), SWIGTYPE_p_stoken_t,0);
        lua_settable(L, -3);
    }
    SWIG_arg += 1;
}


%include "libinjection.h"
