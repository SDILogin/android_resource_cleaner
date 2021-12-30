<h2>Android string resources cleaner</h2>
<p>This project used to simplify removal of unused strings in android projects.</p>

<h3>How to use it</h3>
Run `main.py` with the following configuration 
`-p "$project_dir" --base-xml="$project_dir/src/main/res/values/strings.xml"` 

<h3>Supported params</h3>
`--path, -p` –– path to the project.  
`--base-xml` –– path to the strings.xml in default locale. Walking through project dir to collect all string resources 
not supported yet (not required by target project).  
`--log-level` –– one of the following values: "DEBUG", "INFO", "WARNING", "ERROR". 

<h3>How to adjust</h3>
You need to modify `main.py` if your android project contains multiple string resource files. The key idea 
is to merge all `string.xml` into single xml file. Then this file can be passed as a parameter of 
the cleanup function. 
