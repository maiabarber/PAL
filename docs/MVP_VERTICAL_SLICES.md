# Haver — MVP Vertical Slices Plan

מסמך עבודה למימוש ה-MVP בשיטת **Vertical Slice**: כל Slice נבנה מקצה לקצה לפני שעוברים לבא אחריו.

---

## עקרון העבודה

לא עובדים כך:

```text
כל ה-Backend
    ↓
כל ה-Frontend
    ↓
כל הבדיקות
```

עובדים כך:

```text
Slice אחד
Domain / Use Case
        ↓
Ports
        ↓
Infrastructure
        ↓
FastAPI Endpoint
        ↓
Frontend Page / Component
        ↓
API Integration
        ↓
Tests
        ↓
Commit / PR
```

המטרה: בכל שלב יהיה מוצר קטן אבל עובד, שאפשר להריץ, לבדוק ולהדגים.

---

# ה-Stack שנקבע

## Backend
- Python
- FastAPI
- pytest
- Clean Architecture / Ports & Adapters

## Frontend
- React
- TypeScript
- Responsive Web / PWA
- Mobile-first

## Data & Infrastructure
- Supabase
- PostgreSQL
- Supabase Auth
- Supabase Storage
- RLS

## בהמשך
- Playwright ל-E2E
- React Native / Expo רק אם יהיה צורך באפליקציה Native

---

# מבנה פרויקט מומלץ

```text
haver/
│
├── backend/
│   ├── app/
│   │   ├── domain/
│   │   │   ├── entities/
│   │   │   ├── enums/
│   │   │   └── errors/
│   │   │
│   │   ├── application/
│   │   │   ├── use_cases/
│   │   │   └── dto/
│   │   │
│   │   ├── ports/
│   │   │   ├── repositories/
│   │   │   └── services/
│   │   │
│   │   ├── infrastructure/
│   │   │   ├── repositories/
│   │   │   ├── auth/
│   │   │   ├── storage/
│   │   │   └── supabase/
│   │   │
│   │   ├── presentation/
│   │   │   └── routers/
│   │   │
│   │   └── main.py
│   │
│   └── tests/
│
├── frontend/
│   └── src/
│       ├── pages/
│       ├── components/
│       ├── api/
│       ├── hooks/
│       └── styles/
│
├── docs/
│   ├── diagrams/
│   └── MVP_VERTICAL_SLICES.md
│
└── README.md
```

---

# 10 השלבים שחוזרים בכל Slice

כל Slice נבנה לפי אותה שיטה.

## שלב 1 — מגדירים את ה-Slice

מגדירים:
- מה המשתמש רוצה לבצע.
- איזה Use Case אחראי על זה.
- מה נכנס.
- מה יוצא.
- מה נחשב הצלחה.

דוגמה:

```text
מוצא חיה סורק QR
→ נפתח פרופיל ציבורי
→ מוצגים רק פרטים ציבוריים
→ ניתן ליצור קשר עם הבעלים
```

---

## שלב 2 — Domain

מממשים רק את ישויות ה-Domain הדרושות ל-Slice.

לא בונים מראש את כל המערכת.

לדוגמה:

```text
Pet
Tag
```

ומוסיפים רק חוקים עסקיים שנדרשים כרגע.

---

## שלב 3 — Ports

מגדירים Interfaces שה-Use Case צריך.

לדוגמה:

```text
PetRepository
TagRepository
```

ה-Application לא מכיר Supabase ישירות.

---

## שלב 4 — Use Case + Unit Tests

כותבים את ה-Use Case.

מיד כותבים Unit Tests עם Fake/InMemory repositories.

בודקים:
- Happy path.
- קלט לא חוקי.
- הרשאות.
- מצבי קצה.

---

## שלב 5 — Infrastructure

מממשים את ה-Ports מול Supabase/PostgreSQL.

לדוגמה:

```text
SupabasePetRepository
SupabaseTagRepository
```

כאן בלבד מותר שיהיה קוד כמו:

```python
supabase.table("pets")
```

---

## שלב 6 — API

מוסיפים FastAPI Route.

לדוגמה:

```text
GET /api/v1/public/pets/{public_id}
```

ה-Route:
1. מקבל HTTP request.
2. עושה validation.
3. מפעיל Use Case.
4. מחזיר DTO / response.

אין בו לוגיקה עסקית.

---

## שלב 7 — Frontend UI

בונים את העמוד/הקומפוננטה של אותו Slice.

אפשר קודם להשתמש בנתוני mock כדי לסגור:
- מבנה.
- Responsive.
- RTL.
- Loading.
- Empty state.
- Error state.

---

## שלב 8 — חיבור Frontend ל-API

מוסיפים פונקציה ב:

```text
frontend/src/api/
```

לדוגמה:

```ts
getPublicPet(publicId)
```

והעמוד קורא ל-API האמיתי.

---

## שלב 9 — Integration / E2E

בודקים את הזרימה מקצה לקצה:

```text
UI
↓
API
↓
Use Case
↓
Repository
↓
Supabase
```

ובודקים גם הרשאות.

---

## שלב 10 — Definition of Done + Git

לא עוברים ל-Slice הבא לפני ש:

- הפיצ'ר עובד מקצה לקצה.
- יש Unit Tests.
- יש Integration/API Tests רלוונטיים.
- UI עובד במחשב ובטלפון.
- הרשאות נבדקו.
- שגיאות מטופלות.
- אין secrets בקוד.
- נעשה commit מסודר.
- ה-branch מוכן ל-PR/Merge.

---

# Roadmap — ה-Slices של ה-MVP

---

# Slice 1 — Public QR / NFC Rescue Profile

## מטרה

אדם שמוצא חיה יכול לסרוק QR או להצמיד NFC ולפתוח את הפרופיל הציבורי שלה בלי Login.

## Use Case

```text
GetPublicPetProfileUseCase
```

## Domain

```text
Pet
Tag
TagStatus
```

## Ports

```text
PetRepository
TagRepository
```

## Infrastructure

```text
SupabasePetRepository
SupabaseTagRepository
```

## Database

טבלאות ראשונות:

```text
pets
tags
```

## API

```text
GET /api/v1/public/pets/{public_id}
```

Response לדוגמה:

```json
{
  "status": "active",
  "name": "Luna",
  "photo_url": "...",
  "lost_mode": true,
  "public_notes": "Friendly dog"
}
```

## Frontend

עמוד:

```text
/p/{publicId}
```

להציג:
- תמונה.
- שם.
- מצב Lost.
- הוראות ציבוריות.
- כפתור WhatsApp.

## QR / NFC

שניהם מצביעים לאותו URL:

```text
https://haver.co.il/p/{publicId}
```

## Tests

- publicId לא קיים.
- Tag unclaimed.
- Tag active.
- Tag blocked.
- Pet לא נמצא.
- Lost Mode מוצג.
- מידע רפואי לא נחשף.

## Definition of Done

סריקת QR אמיתית בטלפון פותחת פרופיל ציבורי אמיתי.

---

# Slice 2 — Authentication

## מטרה

בעלים יכול להירשם, להתחבר, להישאר מחובר ולהתנתק.

## Use Cases

```text
RegisterUserUseCase
LoginUserUseCase
LogoutUseCase
GetCurrentUserUseCase
```

## Domain

```text
User
UserRole
```

## Port

```text
AuthPort
```

## Infrastructure

```text
SupabaseAuthAdapter
```

## API

לדוגמה:

```text
POST /api/v1/auth/register
POST /api/v1/auth/login
POST /api/v1/auth/logout
GET  /api/v1/auth/me
```

## Frontend

עמודים:
- Register.
- Login.

קומפוננטות:
- User menu.
- Logout button.
- Protected route handling.

## Tests

- Register תקין.
- Email קיים.
- Password לא תקין.
- Login נכון.
- Login שגוי.
- Logout.
- Endpoint מוגן ללא session.

## Definition of Done

המשתמש יכול להירשם, להתחבר, לרענן את הדף ועדיין להיות מזוהה.

---

# Slice 3 — Owner Pet Management

## מטרה

בעלים יכול ליצור, לראות, לערוך ולמחוק את החיות שלו.

## Use Cases

```text
CreatePetUseCase
GetMyPetsUseCase
UpdatePetUseCase
DeletePetUseCase
```

## Domain

```text
Pet
```

## Port

```text
PetRepository
```

## Infrastructure

```text
SupabasePetRepository
```

## API

```text
POST   /api/v1/pets
GET    /api/v1/pets
GET    /api/v1/pets/{id}
PATCH  /api/v1/pets/{id}
DELETE /api/v1/pets/{id}
```

## Frontend

עמודים:
- Owner Dashboard.
- Add Pet.
- Edit Pet.

להציג:
- רשימת חיות.
- תמונה.
- שם.
- גיל.
- Microchip.
- מצב Lost.
- Edit/Delete.

## Tests

- Create Pet.
- Get My Pets.
- Update Pet.
- Delete Pet.
- Owner A לא רואה Pet של Owner B.
- Owner A לא יכול לערוך Pet של Owner B.

## Definition of Done

משתמש מחובר יכול לנהל רק את החיות שלו דרך האתר.

---

# Slice 4 — Activate Tag

## מטרה

בעלים שקיבל תג חדש יכול להפעיל אותו ולשייך אותו לחיה.

## Use Case

```text
ActivateTagUseCase
```

## Domain

```text
Tag
Pet
TagStatus
```

מעבר מצב:

```text
UNCLAIMED
   ↓
ACTIVE
```

## Ports

```text
TagRepository
PetRepository
```

## API

```text
POST /api/v1/tags/activate
```

Request לדוגמה:

```json
{
  "activation_code": "...",
  "pet_id": "..."
}
```

## Frontend

עמוד:

```text
Activate QR Tag
```

כולל:
- Activation Code.
- בחירת Pet.
- Activate button.
- Success screen.

## Tests

- Code נכון.
- Code שגוי.
- Tag לא קיים.
- Tag כבר פעיל.
- Pet לא שייך למשתמש.
- Activation Code לא נחשף ב-public API.

## Definition of Done

תג אמיתי במצב UNCLAIMED יכול להפוך ל-ACTIVE דרך האתר.

---

# Slice 5 — Lost Mode + Block Tag

## מטרה

בעלים יכול להפעיל מצב אבוד ולחסום תג שאבד או נגנב.

## Use Cases

```text
SetLostModeUseCase
BlockTagUseCase
```

## Domain

```text
Pet.enableLostMode()
Pet.disableLostMode()
Tag.block()
```

## Ports

```text
PetRepository
TagRepository
```

## API

```text
PATCH /api/v1/pets/{id}/lost-mode
POST  /api/v1/tags/{id}/block
```

## Frontend

עמוד:

```text
Pet Settings / Tag Management
```

כולל:
- Lost Mode toggle.
- רשימת tags.
- Tag status.
- Block Tag button.

## Tests

- Lost Mode ON.
- Lost Mode OFF.
- Public profile משתנה בהתאם.
- Block Tag.
- Tag blocked לא מחזיר פרופיל ישן.
- משתמש זר לא משנה Pet/Tag.

## Definition of Done

שינוי Lost Mode בדשבורד משפיע מיד על העמוד הציבורי.

---

# Slice 6 — Medical Timeline

## מטרה

בעלים יכול לצפות בהיסטוריה הרפואית המאומתת של החיה ב-Read Only.

## Use Case

```text
GetMedicalTimelineUseCase
```

## Domain

```text
Vaccination
MedicalNote
```

## Ports

```text
VaccinationRepository
MedicalNoteRepository
```

## Infrastructure

```text
SupabaseVaccinationRepository
SupabaseMedicalNoteRepository
```

## API

```text
GET /api/v1/pets/{id}/medical
```

## Frontend

עמוד:

```text
Medical Timeline
```

להציג:
- חיסונים.
- תאריכים.
- תוקף.
- וטרינר.
- הערות רפואיות.
- Verified status.

## Tests

- Owner רואה timeline של Pet שלו.
- Owner לא רואה Pet של אחר.
- Guest לא רואה מידע רפואי.
- Public profile לעולם לא מחזיר Medical data.

## Definition of Done

Owner יכול לראות מידע רפואי מאומת אבל לא לערוך אותו.

---

# Slice 7 — Veterinarian Medical Write

## מטרה

וטרינר מאומת יכול להוסיף חיסון והערה רפואית.

## Use Cases

```text
AddVaccinationUseCase
AddMedicalNoteUseCase
```

## Domain

```text
Veterinarian
Vaccination
MedicalNote
VerificationStatus
```

## Ports

```text
VeterinarianRepository
VaccinationRepository
MedicalNoteRepository
```

## API

```text
POST /api/v1/vet/pets/{id}/vaccinations
POST /api/v1/vet/pets/{id}/medical-notes
```

## Frontend

עמוד:

```text
Vet Dashboard / Medical Entry
```

כולל:
- Pet summary.
- Vaccination form.
- Medical Note form.
- Vet verified badge.

## Tests

- Verified Vet יכול להוסיף חיסון.
- Verified Vet יכול להוסיף note.
- Vet לא מאומת נחסם.
- Owner נחסם.
- Guest נחסם.
- veterinarianId נשמר ברשומה.

## Definition of Done

וטרינר מאומת מוסיף מידע והבעלים רואה אותו מיד ב-Medical Timeline.

---

# Slice 8 — Admin Veterinarian Verification

## מטרה

Admin יכול לצפות בווטרינרים ממתינים ולאשר או לדחות אותם.

## Use Cases

```text
GetPendingVeterinariansUseCase
VerifyVeterinarianUseCase
RejectVeterinarianUseCase
```

## Domain

```text
Veterinarian
VerificationStatus
```

## Port

```text
VeterinarianRepository
```

## API

```text
GET  /api/v1/admin/veterinarians/pending
POST /api/v1/admin/veterinarians/{id}/verify
POST /api/v1/admin/veterinarians/{id}/reject
```

## Frontend

עמוד:

```text
Admin Veterinarian Verification
```

להציג:
- שם.
- מספר רישיון.
- Clinic.
- Status.
- Approve.
- Reject.

## Tests

- Admin רואה pending.
- Admin מאשר.
- Admin דוחה.
- Owner מקבל 403.
- Vet רגיל מקבל 403.
- Vet approved מקבל גישה ל-medical write.

## Definition of Done

אישור Admin משנה בפועל את הרשאות הווטרינר.

---

# Slice 9 — Storage + Audit

## מטרה

לתמוך בתמונות/מסמכים ולתעד פעולות רגישות.

## Components

```text
StoragePort
SupabaseStorageAdapter

AuditEntry
AuditRepository
SupabaseAuditRepository
```

## Use Cases שיושפעו

לדוגמה:
- Upload Pet Photo.
- Add Vaccination.
- Add Medical Note.
- Verify Veterinarian.
- Block Tag.

## Frontend

- Upload Pet Photo.
- בהמשך Upload Medical Document.
- הצגת upload progress/error.

## Security

- Medical documents ב-private bucket.
- Signed URLs בלבד.
- לא לשמור secrets ב-client.
- Audit immutable.

## Tests

- Upload תקין.
- MIME לא חוקי.
- File גדול מדי.
- Signed URL פג.
- פעולה רפואית יוצרת AuditEntry.
- Block Tag יוצר AuditEntry.

## Definition of Done

פעולות רגישות נרשמות ויש הפרדה בין public files ל-private medical files.

---

# Slice 10 — Hardening + Pilot Readiness

## מטרה

להפוך את ה-MVP ממוצר שעובד למוצר שאפשר לתת למשתמשים אמיתיים.

## E2E Flows

### Flow 1

```text
QR / NFC
↓
Public Profile
↓
WhatsApp
```

### Flow 2

```text
Owner Login
↓
Dashboard
↓
Lost Mode ON
↓
Public Profile changes
```

### Flow 3

```text
Admin approves Vet
↓
Vet Login
↓
Add Vaccination
↓
Owner sees Timeline
```

## Tests

- API Integration.
- RLS.
- Authorization.
- E2E.
- iPhone Safari.
- Android Chrome.
- Desktop Chrome.
- RTL Hebrew.
- Error states.
- Loading states.
- Blocked Tag.
- Invalid publicId.
- Rate limiting בסיסי.

## Operational

- Logging.
- Error monitoring.
- Backup.
- Environment variables.
- Production config.
- Basic analytics.

## Definition of Done

אפשר לתת את המוצר לקבוצת Alpha קטנה ולמדוד שימוש אמיתי.

---

# סדר העבודה בפועל

```text
Prerequisite
Repo + FastAPI + React + /health

        ↓

Slice 1
Public QR / NFC Profile

        ↓

Slice 2
Authentication

        ↓

Slice 3
Pet Management

        ↓

Slice 4
Activate Tag

        ↓

Slice 5
Lost Mode + Block Tag

        ↓

Slice 6
Medical Timeline

        ↓

Slice 7
Vet Medical Write

        ↓

Slice 8
Admin Vet Verification

        ↓

Slice 9
Storage + Audit

        ↓

Slice 10
Hardening + Pilot
```

---

# חוק חשוב לפרויקט

לא מתחילים Slice חדש כאשר הקודם קיים רק ב-Backend.

Slice נחשב גמור רק אם הוא עבר:

```text
Domain
✓

Use Case
✓

Unit Tests
✓

Infrastructure
✓

API
✓

Frontend
✓

API Integration
✓

Authorization
✓

End-to-End Test
✓

Git Commit / PR
✓
```

---

# Branches מומלצים

דוגמה:

```text
main

feature/public-pet-profile
feature/auth
feature/pet-management
feature/tag-activation
feature/lost-mode
feature/medical-timeline
feature/vet-medical-write
feature/admin-vet-verification
feature/storage-audit
feature/mvp-hardening
```

עבור כל Slice:

```text
main
  ↓
feature/<slice-name>
  ↓
development + tests
  ↓
PR
  ↓
merge to main
```

---

# Milestone ראשון

לפני שמתקדמים ל-Authentication:

```text
[ ] FastAPI עובד
[ ] /health עובד
[ ] pytest עובד
[ ] React עובד
[ ] Pet + Tag קיימים
[ ] GetPublicPetProfileUseCase עובד
[ ] Supabase מחובר
[ ] GET public profile עובד
[ ] PublicPetPage קורא ל-API
[ ] Responsive בטלפון
[ ] QR אמיתי פותח אותו
[ ] Test מקצה לקצה עובר
```

רק אז עוברים ל-Slice 2.
