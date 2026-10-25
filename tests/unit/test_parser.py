import pytest
from commit_msg_generator.parser import DiffParser, FileDiff, DiffContent

"""
Tests
- 1 file modified / 1 change
- 1 file modified / 2 changes
- 1 file renamed
- 1 file added
- 1 file deleted
- 2 files modified / 1 change each
- 1 Very large file modified / 500 changes (uv.lock type)
- empty git msg, num_stat, and status
"""
def test_run_one_file_one_line_modification_return_FileDiff():
    # Arrange.
    diff_msg = (
        "diff --git a/src/example.py b/src/example.py\n"
        "index f063189..a2dd04a 100644\n"
        "--- a/src/example.py\n"
        "+++ b/src/example.py\n"
        "@@ -91,4 +91 @@ class Addition:\n"
        "- a = 10\n"
        "+ a = 11"
    )
    diff_stats = (
        "1       1       src/example.py"
    )
    diff_status = (
        "M       src/example.py"
    )
    diff_parser = DiffParser(diff_stats, diff_status, diff_msg)
    expected_diff_class = [
        FileDiff(
            "src/example.py",
            "Modified",
            {"added_lines": 1, "deleted_lines": 1},
            "diff --git a/src/example.py b/src/example.py\nindex f063189..a2dd04a 100644\n--- a/src/example.py\n+++ b/src/example.py\n",
            [
                DiffContent(
                    "@@ -91,4 +91 @@",
                    " class Addition:\n- a = 10\n+ a = 11"
                )
            ]
        )
    ]

    # Act.
    list_of_file_diff = diff_parser.run()

    # Assert.
    assert list_of_file_diff == expected_diff_class

def test_run_contains_git_diff_return_FileDiff():
    # Arrange.
    diff_msg = (
        "diff --git a/eval/diff_cases/A3/diff.txt b/eval/diff_cases/A3/diff.txt\n"
        "new file mode 100644\n"
        "index 0000000..c63f04d\n"
        "--- /dev/null\n"
        "+++ b/eval/diff_cases/A3/diff.txt\n"
        "@@ -0,0 +1,43 @@\n"
        "+diff --git a/packages/common/http/src/xhr.ts b/packages/common/http/src/xhr.ts\n"
        "+index 6a679c72e4..d22ac54374 100644\n"
        "+--- a/packages/common/http/src/xhr.ts\n"
        "++++ b/packages/common/http/src/xhr.ts\n"
        "+@@ -112,8 +112,6 @@ export class HttpXhrBackend implements HttpBackend {\n"
        "+           return headerResponse;\n"
        "+         }\n"
        "+ \n"
        "+-        // Read status and normalize an IE9 bug (https://bugs.jquery.com/ticket/1450).\n"
        "+-        const status: number = xhr.status === 1223 ? HttpStatusCode.NoContent : xhr.status;\n"
        "+         const statusText = xhr.statusText || 'OK';\n"
        "+ \n"
        "+         // Parse headers from XMLHttpRequest - this step is lazy.\n"
        "+@@ -124,7 +122,7 @@ export class HttpXhrBackend implements HttpBackend {\n"
        "+         const url = getResponseUrl(xhr) || req.url;\n"
        "+ \n"
        "+         // Construct the HttpHeaderResponse and memoize it.\n"
        "+-        headerResponse = new HttpHeaderResponse({headers, status, statusText, url});\n"
        "++        headerResponse = new HttpHeaderResponse({headers, status: xhr.status, statusText, url});\n"
        "+         return headerResponse;\n"
        "+       };\n"
        "+ \n"
        "+diff --git a/packages/common/http/test/xhr_spec.ts b/packages/common/http/test/xhr_spec.ts\n"
        "+index 9c513f3f1b..148626b108 100644\n"
        "+--- a/packages/common/http/test/xhr_spec.ts\n"
        "++++ b/packages/common/http/test/xhr_spec.ts\n"
        "+@@ -350,16 +350,6 @@ const XSSI_PREFIX = ')]}\\'\\n';\n"
        "+       });\n"
        "+     });\n"
        "+     describe('corrects for quirks', () => {\n"
        "+-      it('by normalizing 1223 status to 204', done => {\n"
        "+-        backend.handle(TEST_POST).pipe(toArray()).subscribe(events => {\n"
        "+-          expect(events.length).toBe(2);\n"
        "+-          expect(events[1].type).toBe(HttpEventType.Response);\n"
        "+-          const response = events[1] as HttpResponse<string>;\n"
        "+-          expect(response.status).toBe(HttpStatusCode.NoContent);\n"
        "+-          done();\n"
        "+-        });\n"
        "+-        factory.mock.mockFlush(1223, 'IE Special Status', 'Test');\n"
        "+-      });\n"
        "+       it('by normalizing 0 status to 200 if a body is present', done => {\n"
        "+         backend.handle(TEST_POST).pipe(toArray()).subscribe(events => {\n"
        "+           expect(events.length).toBe(2);\n"
    )
    diff_stats = (
        "43      0       eval/diff_cases/A3/diff.txt"
    )
    diff_status = (
        "A       eval/diff_cases/A3/diff.txt"
    )
    diff_parser = DiffParser(diff_stats, diff_status, diff_msg)
    expected_diff_class = [
        FileDiff(
            "eval/diff_cases/A3/diff.txt",
            "Added",
            {"added_lines": 43, "deleted_lines": 0},
            "diff --git a/eval/diff_cases/A3/diff.txt b/eval/diff_cases/A3/diff.txt\nnew file mode 100644\nindex 0000000..c63f04d\n--- /dev/null\n+++ b/eval/diff_cases/A3/diff.txt\n",
            [
                DiffContent(
                    "@@ -0,0 +1,43 @@",
                    "\n"
                    "+diff --git a/packages/common/http/src/xhr.ts b/packages/common/http/src/xhr.ts\n"
                    "+index 6a679c72e4..d22ac54374 100644\n"
                    "+--- a/packages/common/http/src/xhr.ts\n"
                    "++++ b/packages/common/http/src/xhr.ts\n"
                    "+@@ -112,8 +112,6 @@ export class HttpXhrBackend implements HttpBackend {\n"
                    "+           return headerResponse;\n"
                    "+         }\n"
                    "+ \n"
                    "+-        // Read status and normalize an IE9 bug (https://bugs.jquery.com/ticket/1450).\n"
                    "+-        const status: number = xhr.status === 1223 ? HttpStatusCode.NoContent : xhr.status;\n"
                    "+         const statusText = xhr.statusText || 'OK';\n"
                    "+ \n"
                    "+         // Parse headers from XMLHttpRequest - this step is lazy.\n"
                    "+@@ -124,7 +122,7 @@ export class HttpXhrBackend implements HttpBackend {\n"
                    "+         const url = getResponseUrl(xhr) || req.url;\n"
                    "+ \n"
                    "+         // Construct the HttpHeaderResponse and memoize it.\n"
                    "+-        headerResponse = new HttpHeaderResponse({headers, status, statusText, url});\n"
                    "++        headerResponse = new HttpHeaderResponse({headers, status: xhr.status, statusText, url});\n"
                    "+         return headerResponse;\n"
                    "+       };\n"
                    "+ \n"
                    "+diff --git a/packages/common/http/test/xhr_spec.ts b/packages/common/http/test/xhr_spec.ts\n"
                    "+index 9c513f3f1b..148626b108 100644\n"
                    "+--- a/packages/common/http/test/xhr_spec.ts\n"
                    "++++ b/packages/common/http/test/xhr_spec.ts\n"
                    "+@@ -350,16 +350,6 @@ const XSSI_PREFIX = ')]}\\'\\n';\n"
                    "+       });\n"
                    "+     });\n"
                    "+     describe('corrects for quirks', () => {\n"
                    "+-      it('by normalizing 1223 status to 204', done => {\n"
                    "+-        backend.handle(TEST_POST).pipe(toArray()).subscribe(events => {\n"
                    "+-          expect(events.length).toBe(2);\n"
                    "+-          expect(events[1].type).toBe(HttpEventType.Response);\n"
                    "+-          const response = events[1] as HttpResponse<string>;\n"
                    "+-          expect(response.status).toBe(HttpStatusCode.NoContent);\n"
                    "+-          done();\n"
                    "+-        });\n"
                    "+-        factory.mock.mockFlush(1223, 'IE Special Status', 'Test');\n"
                    "+-      });\n"
                    "+       it('by normalizing 0 status to 200 if a body is present', done => {\n"
                    "+         backend.handle(TEST_POST).pipe(toArray()).subscribe(events => {\n"
                    "+           expect(events.length).toBe(2);\n"
                )
            ]
        )
    ]

    # Act.
    list_of_file_diff = diff_parser.run()

    # Assert.
    assert list_of_file_diff == expected_diff_class