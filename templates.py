script_template_cpp_1part = r'constexpr ScriptTemplate %sScriptTemplate("%s.py", "\x01" R"(%s)");'
script_template_cpp_2part = r'const ScriptTemplate * ScriptTemplate::%s() {return &%sScriptTemplate;}'
script_store_cpp = f'addScriptFromTemplate(ScriptTemplate::%s());'
script_template_h = r'static const ScriptTemplate * %s();'
