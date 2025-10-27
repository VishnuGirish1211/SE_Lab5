# SE_Lab5
## Identified Issues Table

| Issue | Type | Line(s) | Description | Fix Approach |
| --- | --- | --- | --- | --- |
| **Dangerous default value []** (Pylint: `W0102`) | Bug | 8 | The `logs=[]` argument is mutable. It will be shared across all calls to `addItem`, causing unexpected behavior. | Change the default to `logs=None` and initialize `if logs is None: logs = []` inside the function. |
| **Use of eval** (Bandit: `B307` / Pylint: `W0123`) | Security (Medium) | 59 | `eval()` is dangerous as it can execute arbitrary code. | Remove the entire line. It's only for demonstration and serves no purpose in the program. |
| **Bare 'except'** (Flake8: `E722` / Pylint: `W0702`) | Bug | 19 | Using `except:` without specifying an exception (a "bare except") catches *all* errors, including system-exit ones, and hides bugs. | Change `except:` to `except KeyError:`, which is the specific error that would happen if the `item` is not in `stock_data`. |
| **'logging' imported but unused** (Flake8: `F401` / Pylint: `W0611`) | Style / Cleanup | 2 | The `logging` module is imported but never used in the code. | Remove the line `import logging`. |
| **Consider using 'with'** (Pylint: `R1732`) | Style / Bug-Risk | 26, 32 | `open()` is used without a `with` statement. If an error happens, the file `f.close()` might not be called, leaving the file open. | Rewrite the `loadData` and `saveData` functions to use `with open(...) as f:`. |
| **consider-using-f-string** (Pylint: `C0209`) | Style | 12 | The code uses old `%` formatting for strings. | Convert the string to an f-string: `f"{datetime.now()}: Added {qty} of {item}"`. |

# Lab 5 Reflection

### 1. Which issues were the easiest to fix, and which were the hardest? [cite_start]Why? [cite: 85]

* **Easiest:** The easiest fixes were removing the unused `logging` import and the dangerous `eval()` call. These were simple because they just involved deleting a line of code and didn't require deep logical changes.
* **Hardest:** The `dangerous-default-value` (`logs=[]`) was the hardest. It required understanding a specific Python concept—that mutable default arguments are shared across all calls. The fix wasn't just a simple syntax change but required changing the function's default to `None` and adding new logic inside to initialize the list.

### [cite_start]2. Did the static analysis tools report any false positives? [cite: 86]

* Initially, Pylint flagged the `global-statement` warning for the `stock_data` variable. While using `global` is often bad practice, it was a necessary part of this specific program's design. This could be considered a "false positive" in the context of this small script, and we suppressed it with a comment.

### [cite_start]3. How would you integrate static analysis tools into your actual software development workflow? [cite: 87, 88]

I would integrate them in two key places:

* **Local Development:** I would configure my code editor (like VS Code) to run Flake8 automatically every time I save a file. This gives me instant feedback on style and simple errors.
* **Continuous Integration (CI):** I would set up a GitHub Action (or similar CI pipeline) to automatically run Pylint and Bandit every time new code is pushed to the repository. This would act as a quality gate, failing the build and blocking a merge if any high-severity security issues (from Bandit) or major bugs (from Pylint) are detected.

### [cite_start]4. What tangible improvements did you observe in the code quality, readability, or potential robustness after applying the fixes? [cite: 89]

* **Robustness:** The code is significantly more robust. Removing `eval()` eliminated a major security vulnerability. Fixing the bare `except` ensures the program won't hide unexpected crashes, and fixing the `load_data` function with `try...except FileNotFoundError` prevents it from crashing if the `inventory.json` file doesn't exist yet.
* **Correctness:** Fixing the mutable `logs=[]` bug was critical. Now, the `addItem` function will work correctly every time and not share logs between different calls, which was a hidden bug.
* **Readability:** The code is much cleaner. Using `with open()` for file handling is more modern and easier to read. Changing string formatting to f-strings also made the code more concise.