# BSD 3-Clause License; see https://github.com/scikit-hep/awkward-1.0/blob/main/LICENSE

import awkward as ak

# C++17 is required for invoke
headers = "functional"
f_cache = {}
f_type = {}


def connect_ArrayBuilder(compiler, builder):
    import ctypes

    f_cache["beginlist"] = f"beginlist_of_{builder._layout._ptr}"
    f_cache["beginrecord"] = f"beginrecord_of_{builder._layout._ptr}"
    f_cache["beginrecord_check"] = f"beginrecord_check_of_{builder._layout._ptr}"
    f_cache["beginrecord_fast"] = f"beginrecord_fast_of_{builder._layout._ptr}"
    f_cache["begintuple"] = f"begintuple_of_{builder._layout._ptr}"
    f_cache["boolean"] = f"boolean_of_{builder._layout._ptr}"
    f_cache["clear"] = f"clear_of_{builder._layout._ptr}"
    f_cache["endlist"] = f"endlist_of_{builder._layout._ptr}"
    f_cache["endrecord"] = f"endrecord_of_{builder._layout._ptr}"
    f_cache["endtuple"] = f"endtuple_of_{builder._layout._ptr}"
    f_cache["field_check"] = f"field_check_of_{builder._layout._ptr}"
    f_cache["field_fast"] = f"field_fast_of_{builder._layout._ptr}"
    f_cache["index"] = f"index_of_{builder._layout._ptr}"
    f_cache["integer"] = f"integer_of_{builder._layout._ptr}"
    f_cache["null"] = f"null_of_{builder._layout._ptr}"
    f_cache["real"] = f"real_of_{builder._layout._ptr}"

    f_type["FuncPtr"] = f"FuncPtr_of_{builder._layout._ptr}"
    f_type["FuncPtr_Int"] = f"FuncPtr_Int_of_{builder._layout._ptr}"
    f_type["FuncPtr_Bool"] = f"FuncPtr_Bool_of_{builder._layout._ptr}"
    f_type["FuncPtr_Dbl"] = f"FuncPtr_Dbl_of_{builder._layout._ptr}"
    f_type["FuncPtr_CharPtr"] = f"FuncPtr_CharPtr_of_{builder._layout._ptr}"

    out = f"""
    typedef uint8_t (*{f_type["FuncPtr"]})(void*);
    typedef uint8_t (*{f_type["FuncPtr_Int"]})(void*, int64_t);
    typedef uint8_t (*{f_type["FuncPtr_Bool"]})(void*, bool);
    typedef uint8_t (*{f_type["FuncPtr_Dbl"]})(void*, double);
    typedef uint8_t (*{f_type["FuncPtr_CharPtr"]})(void*, const char*);

    uint8_t
    {f_cache["beginlist"]}() {{
        return std::invoke(reinterpret_cast<{f_type["FuncPtr"]}>(reinterpret_cast<long>({ctypes.cast(ak._libawkward.ArrayBuilder_beginlist, ctypes.c_voidp).value})), reinterpret_cast<void *>({builder._layout._ptr}));
    }}

    uint8_t
    {f_cache["beginrecord"]}() {{
        return std::invoke(reinterpret_cast<{f_type["FuncPtr"]}>(reinterpret_cast<long>({ctypes.cast(ak._libawkward.ArrayBuilder_beginrecord, ctypes.c_voidp).value})), reinterpret_cast<void *>({builder._layout._ptr}));
    }}

    uint8_t
    {f_cache["beginrecord_check"]}(const char* name) {{
        return std::invoke(reinterpret_cast<{f_type["FuncPtr_CharPtr"]}>(reinterpret_cast<long>({ctypes.cast(ak._libawkward.ArrayBuilder_beginrecord_check, ctypes.c_voidp).value})), reinterpret_cast<void *>({builder._layout._ptr}), name);
    }}

    uint8_t
    {f_cache["beginrecord_fast"]}(const char* name) {{
        return std::invoke(reinterpret_cast<{f_type["FuncPtr_CharPtr"]}>(reinterpret_cast<long>({ctypes.cast(ak._libawkward.ArrayBuilder_beginrecord_fast, ctypes.c_voidp).value})), reinterpret_cast<void *>({builder._layout._ptr}), name);
    }}

    uint8_t
    {f_cache["begintuple"]}(int64_t numfields) {{
        return std::invoke(reinterpret_cast<{f_type["FuncPtr_Int"]}>(reinterpret_cast<long>({ctypes.cast(ak._libawkward.ArrayBuilder_begintuple, ctypes.c_voidp).value})), reinterpret_cast<void *>({builder._layout._ptr}), numfields);
    }}

    uint8_t
    {f_cache["boolean"]}(bool x) {{
        return std::invoke(reinterpret_cast<{f_type["FuncPtr_Bool"]}>(reinterpret_cast<long>({ctypes.cast(ak._libawkward.ArrayBuilder_boolean, ctypes.c_void_p).value})), reinterpret_cast<void *>({builder._layout._ptr}), x);
    }}

    uint8_t
    {f_cache["clear"]}() {{
        return std::invoke(reinterpret_cast<{f_type["FuncPtr"]}>(reinterpret_cast<long>({ctypes.cast(ak._libawkward.ArrayBuilder_clear, ctypes.c_void_p).value})), reinterpret_cast<void *>({builder._layout._ptr}));
    }}

    uint8_t
    {f_cache["endlist"]}() {{
        return std::invoke(reinterpret_cast<{f_type["FuncPtr"]}>(reinterpret_cast<long>({ctypes.cast(ak._libawkward.ArrayBuilder_endlist, ctypes.c_void_p).value})), reinterpret_cast<void *>({builder._layout._ptr}));
    }}

    uint8_t
    {f_cache["endrecord"]}() {{
        return std::invoke(reinterpret_cast<{f_type["FuncPtr"]}>(reinterpret_cast<long>({ctypes.cast(ak._libawkward.ArrayBuilder_endrecord, ctypes.c_void_p).value})), reinterpret_cast<void *>({builder._layout._ptr}));
    }}

    uint8_t
    {f_cache["endtuple"]}() {{
        return std::invoke(reinterpret_cast<{f_type["FuncPtr"]}>(reinterpret_cast<long>({ctypes.cast(ak._libawkward.ArrayBuilder_endtuple, ctypes.c_void_p).value})), reinterpret_cast<void *>({builder._layout._ptr}));
    }}

    uint8_t
    {f_cache["field_check"]}(const char* key) {{
        return std::invoke(reinterpret_cast<{f_type["FuncPtr_CharPtr"]}>(reinterpret_cast<long>({ctypes.cast(ak._libawkward.ArrayBuilder_field_check, ctypes.c_void_p).value})), reinterpret_cast<void *>({builder._layout._ptr}), key);
    }}

    uint8_t
    {f_cache["field_fast"]}(const char* key) {{
        return std::invoke(reinterpret_cast<{f_type["FuncPtr_CharPtr"]}>(reinterpret_cast<long>({ctypes.cast(ak._libawkward.ArrayBuilder_field_fast, ctypes.c_void_p).value})), reinterpret_cast<void *>({builder._layout._ptr}), key);
    }}

    uint8_t
    {f_cache["index"]}(int64_t index) {{
        return std::invoke(reinterpret_cast<{f_type["FuncPtr_Int"]}>(reinterpret_cast<long>({ctypes.cast(ak._libawkward.ArrayBuilder_index, ctypes.c_void_p).value})), reinterpret_cast<void *>({builder._layout._ptr}), index);
    }}

    uint8_t
    {f_cache["integer"]}(int64_t x) {{
        return std::invoke(reinterpret_cast<{f_type["FuncPtr_Int"]}>(reinterpret_cast<long>({ctypes.cast(ak._libawkward.ArrayBuilder_integer, ctypes.c_void_p).value})), reinterpret_cast<void *>({builder._layout._ptr}), x);
    }}

    uint8_t
    {f_cache["null"]}() {{
        return std::invoke(reinterpret_cast<{f_type["FuncPtr"]}>(reinterpret_cast<long>({ctypes.cast(ak._libawkward.ArrayBuilder_null, ctypes.c_void_p).value})), reinterpret_cast<void *>({builder._layout._ptr}));
    }}

    uint8_t
    {f_cache["real"]}(double x) {{
        return std::invoke(reinterpret_cast<{f_type["FuncPtr_Dbl"]}>(reinterpret_cast<long>({ctypes.cast(ak._libawkward.ArrayBuilder_real, ctypes.c_void_p).value})), reinterpret_cast<void *>({builder._layout._ptr}), x);
    }}
    """.strip()
    compiler(out)
    return f_cache
