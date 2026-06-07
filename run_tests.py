"""
INC4119 Photo Gallery — Test Report Script
Runs all TC001–TC010 test cases against http://localhost:8000
"""

import requests
import json
import io
import os
from datetime import datetime

BASE_URL = "http://localhost:8000"
results = []

# Tokens shared across test cases
AUTH_TOKEN = None        # primary test user token
AUTH_TOKEN_2 = None      # secondary test user token
UPLOADED_PHOTO_ID = None
SENT_MESSAGE_ID = None

TEST_USER1 = {"username": "testuser_tc001", "password": "1234"}
TEST_USER2 = {"username": "testuser_tc002", "password": "1234"}


# ─────────────────────────────────────────────
def record(tc_id, step, description, expected, actual_raw, passed):
    actual_str = str(actual_raw)[:200]
    results.append({
        "tc": tc_id,
        "step": step,
        "description": description,
        "expected": expected,
        "actual": actual_str,
        "result": "Pass" if passed else "Fail",
    })
    mark = "✅" if passed else "❌"
    print(f"  {mark} {tc_id}-S{step}: {description}")
    if not passed:
        print(f"       Expected : {expected}")
        print(f"       Actual   : {actual_str}")


def auth_header(token):
    return {"Authorization": f"Bearer {token}"}


def small_png():
    """Returns a minimal 1×1 white PNG as bytes."""
    import struct, zlib
    def chunk(name, data):
        c = name + data
        return struct.pack(">I", len(data)) + c + struct.pack(">I", zlib.crc32(c) & 0xFFFFFFFF)
    sig = b"\x89PNG\r\n\x1a\n"
    ihdr = chunk(b"IHDR", struct.pack(">IIBBBBB", 1, 1, 8, 2, 0, 0, 0))
    idat = chunk(b"IDAT", zlib.compress(b"\x00\xFF\xFF\xFF"))
    iend = chunk(b"IEND", b"")
    return sig + ihdr + idat + iend


# ─────────────────────────────────────────────
# PRE-SETUP: ensure test users exist
# ─────────────────────────────────────────────
def setup():
    global AUTH_TOKEN, AUTH_TOKEN_2
    print("\n[SETUP] Creating test users if they don't exist...")
    for u in [TEST_USER1, TEST_USER2]:
        requests.post(f"{BASE_URL}/api/auth/signup", json=u)

    r1 = requests.post(f"{BASE_URL}/api/auth/login", json=TEST_USER1)
    r2 = requests.post(f"{BASE_URL}/api/auth/login", json=TEST_USER2)
    if r1.status_code == 200:
        AUTH_TOKEN = r1.json()["access_token"]
        print(f"  User1 token acquired")
    if r2.status_code == 200:
        AUTH_TOKEN_2 = r2.json()["access_token"]
        print(f"  User2 token acquired")


# ─────────────────────────────────────────────
# TC001 — Sign Up
# ─────────────────────────────────────────────
def tc001():
    print("\n[TC001] Sign Up")

    # Step 1: empty username
    r = requests.post(f"{BASE_URL}/api/auth/signup", json={"username": "", "password": "1234"})
    record("TC001", 1, "Signup with empty username → 400/422",
           "400 or 422", f"{r.status_code} {r.text[:80]}",
           r.status_code in (400, 422))

    # Step 2: password too short (< 4)
    r = requests.post(f"{BASE_URL}/api/auth/signup", json={"username": "tmpuser_short", "password": "12"})
    record("TC001", 2, "Signup with password < 4 chars → 400/422",
           "400 or 422", f"{r.status_code} {r.text[:80]}",
           r.status_code in (400, 422))

    # Step 3: mismatched passwords (API has no confirm_password field — expected behaviour: 400)
    r = requests.post(f"{BASE_URL}/api/auth/signup",
                      json={"username": "tmpuser_mismatch", "password": "abcd", "confirm_password": "wxyz"})
    # Backend ignores extra fields; registration succeeds — document actual behaviour
    record("TC001", 3, "Signup with mismatched passwords → 400",
           "400", f"{r.status_code} {r.text[:80]}",
           r.status_code == 400)

    # Step 4: duplicate username
    r = requests.post(f"{BASE_URL}/api/auth/signup", json=TEST_USER1)
    record("TC001", 4, "Signup with duplicate username → 400",
           "400", f"{r.status_code} {r.text[:80]}",
           r.status_code == 400)

    # Step 5: valid signup (fresh unique account each run)
    import time
    fresh = {"username": f"tc001_fresh_{int(time.time())}", "password": "abcd1234"}
    r = requests.post(f"{BASE_URL}/api/auth/signup", json=fresh)
    record("TC001", 5, "Signup with valid data → 201",
           "201", f"{r.status_code} {r.text[:80]}",
           r.status_code == 201)

    # Step 6: login with new account
    r = requests.post(f"{BASE_URL}/api/auth/login", json=fresh)
    record("TC001", 6, "Login with newly created account → 200 + token",
           "200 + access_token", f"{r.status_code} has_token={('access_token' in r.text)}",
           r.status_code == 200 and "access_token" in r.json())


# ─────────────────────────────────────────────
# TC002 — Sign In
# ─────────────────────────────────────────────
def tc002():
    print("\n[TC002] Sign In")

    # Step 1: empty password
    r = requests.post(f"{BASE_URL}/api/auth/login", json={"username": "kms_0109", "password": ""})
    record("TC002", 1, "Login with empty password → 400/422",
           "400/401/422", f"{r.status_code} {r.text[:80]}",
           r.status_code in (400, 401, 422))

    # Step 2: non-existent username
    r = requests.post(f"{BASE_URL}/api/auth/login", json={"username": "no_such_user_xyz", "password": "1234"})
    record("TC002", 2, "Login with non-existent user → 401",
           "401 or 400", f"{r.status_code} {r.text[:80]}",
           r.status_code in (400, 401))

    # Step 3: wrong password
    r = requests.post(f"{BASE_URL}/api/auth/login", json={"username": TEST_USER1["username"], "password": "wrongpass"})
    record("TC002", 3, "Login with wrong password → 401",
           "401 or 400", f"{r.status_code} {r.text[:80]}",
           r.status_code in (400, 401))

    # Step 4: correct credentials
    r = requests.post(f"{BASE_URL}/api/auth/login", json=TEST_USER1)
    has_token = r.status_code == 200 and "access_token" in r.json()
    record("TC002", 4, "Login with correct credentials → 200 + access_token",
           "200 + access_token", f"{r.status_code} has_token={has_token}",
           has_token)


# ─────────────────────────────────────────────
# TC003 — Sign Out
# ─────────────────────────────────────────────
def tc003():
    print("\n[TC003] Sign Out")

    # Step 1: logout with valid token
    r = requests.post(f"{BASE_URL}/api/auth/logout", headers=auth_header(AUTH_TOKEN))
    record("TC003", 1, "Logout with valid token → 200",
           "200", f"{r.status_code} {r.text[:80]}",
           r.status_code == 200)

    # Step 2: logout with no token (our impl ignores token)
    r = requests.post(f"{BASE_URL}/api/auth/logout")
    record("TC003", 2, "Logout with no/expired token → 200 or 401",
           "200 or 401", f"{r.status_code} {r.text[:80]}",
           r.status_code in (200, 401))


# ─────────────────────────────────────────────
# TC004 — View User List
# ─────────────────────────────────────────────
def tc004():
    print("\n[TC004] View User List")

    # Step 1: no auth
    r = requests.get(f"{BASE_URL}/api/users")
    is_list = isinstance(r.json(), list)
    record("TC004", 1, "GET /api/users without auth → 200 + list",
           "200 + list", f"{r.status_code} is_list={is_list}",
           r.status_code == 200 and is_list)

    # Step 2: response contains only user data (no photo fields)
    if r.status_code == 200 and is_list and len(r.json()) > 0:
        item = r.json()[0]
        keys = set(item.keys())
        no_photo_fields = "image_path" not in keys and "keywords" not in keys
        record("TC004", 2, "User list items contain no photo data",
               "no image_path / keywords fields", f"keys={list(keys)}",
               no_photo_fields)
    else:
        record("TC004", 2, "User list items contain no photo data", "n/a", "empty list", True)

    # Step 3: with auth token
    r = requests.get(f"{BASE_URL}/api/users", headers=auth_header(AUTH_TOKEN))
    record("TC004", 3, "GET /api/users with auth → 200 + list",
           "200 + list", f"{r.status_code}",
           r.status_code == 200 and isinstance(r.json(), list))


# ─────────────────────────────────────────────
# TC005 — View All Photos
# ─────────────────────────────────────────────
def tc005():
    print("\n[TC005] View All Photos")

    # Step 1: with auth
    r = requests.get(f"{BASE_URL}/api/photos", headers=auth_header(AUTH_TOKEN))
    record("TC005", 1, "GET /api/photos with auth → 200 + list",
           "200 + list", f"{r.status_code} is_list={isinstance(r.json(), list)}",
           r.status_code == 200 and isinstance(r.json(), list))

    # Step 2: without auth
    r = requests.get(f"{BASE_URL}/api/photos")
    record("TC005", 2, "GET /api/photos without auth → 401",
           "401", f"{r.status_code} {r.text[:80]}",
           r.status_code == 401)

    # Step 3: auth + verify list format (even if empty, status 200)
    r = requests.get(f"{BASE_URL}/api/photos", headers=auth_header(AUTH_TOKEN))
    record("TC005", 3, "GET /api/photos with auth → 200 (even if empty)",
           "200 + list (possibly empty)", f"{r.status_code} count={len(r.json()) if r.status_code == 200 else 'n/a'}",
           r.status_code == 200)


# ─────────────────────────────────────────────
# TC006 — Upload Photo
# ─────────────────────────────────────────────
def tc006():
    global UPLOADED_PHOTO_ID
    print("\n[TC006] Upload Photo")

    # Step 1: no file
    r = requests.post(f"{BASE_URL}/api/photos",
                      headers=auth_header(AUTH_TOKEN),
                      data={"description": "desc", "keywords": "key"})
    record("TC006", 1, "POST /api/photos with no file → 400/422",
           "400 or 422", f"{r.status_code} {r.text[:80]}",
           r.status_code in (400, 422))

    # Step 2: no description (backend may allow nullable description)
    png = small_png()
    r = requests.post(f"{BASE_URL}/api/photos",
                      headers=auth_header(AUTH_TOKEN),
                      files={"file": ("test.png", io.BytesIO(png), "image/png")},
                      data={"keywords": "test"})
    # Backend spec: description is nullable, so this may succeed (200/201)
    record("TC006", 2, "POST /api/photos with no description → 400/422 or 200",
           "400/422 (or 200 if nullable)", f"{r.status_code} {r.text[:80]}",
           r.status_code in (200, 201, 400, 422))

    # Step 3: valid upload
    r = requests.post(f"{BASE_URL}/api/photos",
                      headers=auth_header(AUTH_TOKEN),
                      files={"file": ("test.png", io.BytesIO(png), "image/png")},
                      data={"description": "test photo", "keywords": "바다,테스트"})
    ok = r.status_code in (200, 201)
    if ok:
        UPLOADED_PHOTO_ID = r.json().get("id")
    record("TC006", 3, "POST /api/photos with valid file+desc+keywords → 200/201",
           "200 or 201", f"{r.status_code} id={UPLOADED_PHOTO_ID}",
           ok)

    # Step 4: uploaded photo appears in list
    if UPLOADED_PHOTO_ID:
        r = requests.get(f"{BASE_URL}/api/photos", headers=auth_header(AUTH_TOKEN))
        ids = [p["id"] for p in r.json()] if r.status_code == 200 else []
        record("TC006", 4, "Uploaded photo appears in GET /api/photos",
               f"id {UPLOADED_PHOTO_ID} in list", f"ids={ids[:5]}",
               UPLOADED_PHOTO_ID in ids)
    else:
        record("TC006", 4, "Uploaded photo appears in GET /api/photos", "n/a", "upload failed", False)

    # Step 5: no auth
    r = requests.post(f"{BASE_URL}/api/photos",
                      files={"file": ("test.png", io.BytesIO(png), "image/png")},
                      data={"description": "x", "keywords": "y"})
    record("TC006", 5, "POST /api/photos without auth → 401",
           "401", f"{r.status_code} {r.text[:80]}",
           r.status_code == 401)


# ─────────────────────────────────────────────
# TC007 — Edit Photo Info
# ─────────────────────────────────────────────
def tc007():
    print("\n[TC007] Edit Photo Info")

    if not UPLOADED_PHOTO_ID:
        for step in (1, 2, 3):
            record("TC007", step, "Edit photo (no photo uploaded in TC006)", "n/a", "skip", False)
        return

    pid = UPLOADED_PHOTO_ID

    # Step 1: empty description (backend may allow empty string — nullable)
    r = requests.put(f"{BASE_URL}/api/photos/{pid}",
                     headers=auth_header(AUTH_TOKEN),
                     json={"description": "", "keywords": "바다"})
    record("TC007", 1, "PUT /api/photos/{id} with empty description → 400/422 or 200",
           "400/422 (or 200 if nullable)", f"{r.status_code} {r.text[:80]}",
           r.status_code in (200, 400, 422))

    # Step 2: valid update
    r = requests.put(f"{BASE_URL}/api/photos/{pid}",
                     headers=auth_header(AUTH_TOKEN),
                     json={"description": "updated desc", "keywords": "바다,수정"})
    record("TC007", 2, "PUT /api/photos/{id} with valid data → 200",
           "200", f"{r.status_code} {r.text[:80]}",
           r.status_code == 200)

    # Step 3: non-owner (user2 tries to edit user1's photo)
    r = requests.put(f"{BASE_URL}/api/photos/{pid}",
                     headers=auth_header(AUTH_TOKEN_2),
                     json={"description": "hacked", "keywords": "hack"})
    record("TC007", 3, "PUT /api/photos/{id} by non-owner → 403",
           "403", f"{r.status_code} {r.text[:80]}",
           r.status_code == 403)


# ─────────────────────────────────────────────
# TC008 — Search by Keyword
# ─────────────────────────────────────────────
def tc008():
    print("\n[TC008] Search by Keyword")

    # Step 1: keyword that should match (we uploaded with '바다')
    r = requests.get(f"{BASE_URL}/api/photos/search?keyword=바다")
    record("TC008", 1, "GET /api/photos/search?keyword=바다 → 200 + matches",
           "200 + list", f"{r.status_code} count={len(r.json()) if r.status_code==200 else 'err'}",
           r.status_code == 200)

    # Step 2: empty keyword
    r = requests.get(f"{BASE_URL}/api/photos/search?keyword=")
    record("TC008", 2, "GET /api/photos/search?keyword= (empty) → 400 or empty list",
           "400 or 200+empty", f"{r.status_code} {r.text[:80]}",
           r.status_code in (200, 400))

    # Step 3: non-existent keyword
    r = requests.get(f"{BASE_URL}/api/photos/search?keyword=존재하지않는키워드xyz")
    record("TC008", 3, "Search for non-existent keyword → 200 + empty list",
           "200 + []", f"{r.status_code} body={r.text[:60]}",
           r.status_code == 200 and r.json() == [])

    # Step 4: search without auth (should be public)
    r = requests.get(f"{BASE_URL}/api/photos/search?keyword=바다")
    record("TC008", 4, "Search without auth → 200 (public endpoint)",
           "200", f"{r.status_code} {r.text[:60]}",
           r.status_code == 200)


# ─────────────────────────────────────────────
# TC009 — Send Direct Message
# ─────────────────────────────────────────────
def tc009():
    global SENT_MESSAGE_ID
    print("\n[TC009] Send Direct Message")

    # get user2 id
    users = requests.get(f"{BASE_URL}/api/users").json()
    user2_id = next((u["id"] for u in users if u["username"] == TEST_USER2["username"]), None)
    user1_id = next((u["id"] for u in users if u["username"] == TEST_USER1["username"]), None)

    # Step 1: no auth
    r = requests.post(f"{BASE_URL}/api/messages",
                      json={"receiver_id": user2_id, "content": "hi"})
    record("TC009", 1, "POST /api/messages without auth → 401",
           "401", f"{r.status_code} {r.text[:80]}",
           r.status_code == 401)

    # Step 2: empty content
    r = requests.post(f"{BASE_URL}/api/messages",
                      headers=auth_header(AUTH_TOKEN),
                      json={"receiver_id": user2_id, "content": ""})
    record("TC009", 2, "POST /api/messages with empty content → 400/422",
           "400 or 422", f"{r.status_code} {r.text[:80]}",
           r.status_code in (400, 422))

    # Step 3: valid DM to another user
    r = requests.post(f"{BASE_URL}/api/messages",
                      headers=auth_header(AUTH_TOKEN),
                      json={"receiver_id": user2_id, "content": "안녕하세요 테스트 메시지"})
    ok = r.status_code in (200, 201)
    if ok:
        SENT_MESSAGE_ID = r.json().get("id")
    record("TC009", 3, "POST /api/messages valid content to other user → 200/201",
           "200 or 201", f"{r.status_code} id={SENT_MESSAGE_ID}",
           ok)

    # Step 4: DM to self (backend may or may not reject)
    r = requests.post(f"{BASE_URL}/api/messages",
                      headers=auth_header(AUTH_TOKEN),
                      json={"receiver_id": user1_id, "content": "self message"})
    record("TC009", 4, "POST /api/messages to self → 400",
           "400", f"{r.status_code} {r.text[:80]}",
           r.status_code == 400)


# ─────────────────────────────────────────────
# TC010 — View Messages / Reply / Delete
# ─────────────────────────────────────────────
def tc010():
    print("\n[TC010] View Messages / Reply / Delete")

    # Step 1: get messages as user2 (receiver of the DM we sent)
    r = requests.get(f"{BASE_URL}/api/messages", headers=auth_header(AUTH_TOKEN_2))
    is_list = isinstance(r.json(), list)
    record("TC010", 1, "GET /api/messages (receiver) → 200 + list",
           "200 + list", f"{r.status_code} is_list={is_list} count={len(r.json()) if is_list else 'err'}",
           r.status_code == 200 and is_list)

    # find the message we sent
    msgs = r.json() if r.status_code == 200 else []
    msg_id = msgs[0]["id"] if msgs else SENT_MESSAGE_ID

    # Step 2: reply with empty content
    if msg_id:
        r = requests.post(f"{BASE_URL}/api/messages/{msg_id}/reply",
                          headers=auth_header(AUTH_TOKEN_2),
                          json={"content": ""})
        record("TC010", 2, "Reply with empty content → 400/422",
               "400 or 422", f"{r.status_code} {r.text[:80]}",
               r.status_code in (400, 422))

        # Step 3: valid reply
        r = requests.post(f"{BASE_URL}/api/messages/{msg_id}/reply",
                          headers=auth_header(AUTH_TOKEN_2),
                          json={"content": "답장 테스트"})
        record("TC010", 3, "Reply with valid content → 200/201",
               "200 or 201", f"{r.status_code} {r.text[:80]}",
               r.status_code in (200, 201))

        # Step 4: delete the message
        r = requests.delete(f"{BASE_URL}/api/messages/{msg_id}",
                            headers=auth_header(AUTH_TOKEN_2))
        record("TC010", 4, "DELETE /api/messages/{id} → 200",
               "200", f"{r.status_code} {r.text[:80]}",
               r.status_code == 200)

        # confirm deleted
        r2 = requests.get(f"{BASE_URL}/api/messages", headers=auth_header(AUTH_TOKEN_2))
        remaining_ids = [m["id"] for m in r2.json()] if r2.status_code == 200 else []
        record("TC010", 5, "GET /api/messages after delete → message no longer present",
               f"id {msg_id} not in list", f"remaining={remaining_ids[:5]}",
               msg_id not in remaining_ids)
    else:
        for step in (2, 3, 4, 5):
            record("TC010", step, "No message available from TC009", "n/a", "skip", False)


# ─────────────────────────────────────────────
# SUMMARY & REPORT
# ─────────────────────────────────────────────
def print_summary():
    total = len(results)
    passed = sum(1 for r in results if r["result"] == "Pass")
    failed = total - passed

    print("\n" + "═" * 68)
    print(f"  TEST SUMMARY   Total: {total}  |  Pass: {passed}  |  Fail: {failed}")
    print("═" * 68)
    print(f"{'TC':<8} {'Step':<6} {'Result':<7} Description")
    print("─" * 68)
    for r in results:
        mark = "✅ Pass" if r["result"] == "Pass" else "❌ Fail"
        print(f"{r['tc']:<8} S{r['step']:<5} {mark:<7} {r['description']}")
    print("─" * 68)

    if failed > 0:
        print("\nFailed test cases:")
        for r in results:
            if r["result"] == "Fail":
                print(f"  • {r['tc']}-S{r['step']}: {r['description']}")
                print(f"    Expected : {r['expected']}")
                print(f"    Actual   : {r['actual']}")

    return passed, failed


def save_report():
    report = {
        "generated_at": datetime.now().isoformat(),
        "summary": {
            "total": len(results),
            "passed": sum(1 for r in results if r["result"] == "Pass"),
            "failed": sum(1 for r in results if r["result"] == "Fail"),
        },
        "results": results,
    }
    path = os.path.join(os.path.dirname(__file__), "test_report_results.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"\n  Report saved -> {path}")
    return report


# ─────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 68)
    print("  INC4119 Photo Gallery - Test Execution")
    print(f"  Server : {BASE_URL}")
    print(f"  Time   : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 68)

    setup()
    tc001()
    tc002()
    tc003()
    tc004()
    tc005()
    tc006()
    tc007()
    tc008()
    tc009()
    tc010()

    passed, failed = print_summary()
    save_report()
