# Linux Command-Line Basics — Assignment Submission

A walkthrough of 7 core Linux/Unix command-line tasks, each with the exact command used, the actual output, and an explanation.

> Environment note: Run on macOS (zsh). All commands are standard POSIX/Linux commands. The one exception is `wget`, which is not bundled with macOS — the macOS equivalent `curl` is shown, plus how to install `wget`.

---

## 1. Creating and Renaming Files/Directories

**Commands**
```bash
mkdir test_dir                 # create a directory
touch test_dir/example.txt     # create an empty file inside it
mv test_dir/example.txt test_dir/renamed_example.txt   # rename the file
```

**Output**
```
--- before rename ---
-rw-r--r--  1 user  staff  0  example.txt
--- after rename ---
-rw-r--r--  1 user  staff  0  renamed_example.txt
```

**Explanation**
- `mkdir` ("make directory") creates a new folder.
- `touch` creates an empty file (or updates the timestamp if it already exists).
- `mv` ("move") moves a file; when source and destination are in the same directory, it effectively **renames** the file.

---

## 2. Viewing File Contents

**Commands**
```bash
cat /etc/passwd        # print the entire file
head -5 /etc/passwd    # first 5 lines
tail -5 /etc/passwd    # last 5 lines
```

**Output (head -5)**
```
##
# User Database
#
# Note that this file is consulted directly only when the system is running
# in single-user mode.  At other times this information is provided by
```

**Output (tail -5)**
```
_spinandd:*:305:305:SPINAND Daemon:/var/empty:/usr/bin/false
_corespeechd:*:306:306:CoreSpeech Services:/var/empty:/usr/bin/false
_diagnosticservicesd:*:307:307:Diagnostic Services:/var/empty:/usr/bin/false
_mds_stores:*:308:308:Spotlight File Metadata Index Daemon:/var/empty:/usr/bin/false
_oahd:*:441:441:OAH Daemon:/var/empty:/usr/bin/false
```

**Explanation**
- `cat` ("concatenate") dumps the whole file to the screen.
- `head -5` shows only the **first** 5 lines — useful for previewing big files.
- `tail -5` shows only the **last** 5 lines — useful for reading the newest log entries.
- `/etc/passwd` lists user accounts; each line is `username:password:UID:GID:description:home:shell`.

---

## 3. Searching for Patterns

**Command**
```bash
grep "root" /etc/passwd
```

**Output**
```
root:*:0:0:System Administrator:/var/root:/bin/sh
daemon:*:1:1:System Services:/var/root:/usr/bin/false
_cvmsroot:*:212:212:CVMS Root:/var/empty:/usr/bin/false
```

**Explanation**
`grep` ("global regular expression print") scans a file line by line and prints every line containing the pattern. Here it returns all lines mentioning `root`. Add `-i` for case-insensitive, `-n` to show line numbers, `-r` to search a whole directory.

---

## 4. Zipping and Unzipping

**Commands**
```bash
zip -r test_dir.zip test_dir          # compress the directory
unzip -o test_dir.zip -d unzipped_dir # extract into a new directory
```

**Output**
```
  adding: test_dir/ (stored 0%)
  adding: test_dir/renamed_example.txt (stored 0%)
Archive:  test_dir.zip
   creating: unzipped_dir/test_dir
 extracting: unzipped_dir/test_dir/renamed_example.txt
```

**Explanation**
- `zip -r` compresses a directory into a single `.zip` archive; `-r` means **recursive** (include all sub-files/folders).
- `unzip -d` extracts an archive into a target directory (`-o` overwrites without prompting).

---

## 5. Downloading Files

**Command (Linux)**
```bash
wget https://example.com/sample.txt
```

**macOS equivalent (wget not preinstalled)**
```bash
curl -L -o sample.html https://example.com
```

**Output**
```
-rw-r--r--  1 user  staff  559  sample.html
<!doctype html><html lang="en"><head><title>Example Domain</title>...
```

**Explanation**
`wget` downloads files from a URL over HTTP/HTTPS/FTP. On macOS it isn't installed by default, so `curl -L -o <file> <url>` does the same job (`-L` follows redirects, `-o` sets the output filename).
To install real `wget` on macOS: `brew install wget`.

---

## 6. Changing Permissions

**Commands**
```bash
echo "some secret content" > secure.txt
chmod 444 secure.txt          # read-only for owner, group, and others
```

**Output**
```
--- before ---  -rw-r--r--   secure.txt
--- after  ---  -r--r--r--   secure.txt
# Attempting to write:
permission denied: secure.txt   <-- write blocked as expected
```

**Explanation**
`chmod` ("change mode") sets file permissions. The octal `444` means **read (4) only** for all three identity classes (owner / group / others) and no write or execute. After this, even the owner cannot modify the file until permissions are restored (e.g. `chmod 644`).

Permission digits: read = 4, write = 2, execute = 1 (added together per class).

---

## 7. Working with Environment Variables

**Commands**
```bash
export MY_VAR="Hello, Linux!"
echo $MY_VAR
env | grep MY_VAR
```

**Output**
```
Hello, Linux!
MY_VAR=Hello, Linux!
```

**Explanation**
`export` defines an **environment variable** and makes it available to the current shell and any child processes it launches. `echo $MY_VAR` prints its value; `env` lists all environment variables. Note: this lasts only for the current terminal session — to make it permanent, add the `export` line to `~/.zshrc` or `~/.bashrc`.

---

## Summary Table

| # | Task | Key Command(s) |
|---|------|----------------|
| 1 | Create & rename | `mkdir`, `touch`, `mv` |
| 2 | View contents | `cat`, `head -5`, `tail -5` |
| 3 | Search patterns | `grep "root" /etc/passwd` |
| 4 | Zip / unzip | `zip -r`, `unzip -d` |
| 5 | Download | `wget` / `curl -L -o` |
| 6 | Permissions | `chmod 444` |
| 7 | Env variables | `export MY_VAR=...` |
