# Spy Cat Agency API

API to control cats spy missions

---

## Local run

```bash

1.git clone https://github.com/maksymmatsapura41-droid/Spy-Cat-Agency-DT.git
2.python -m venv venv
3.source venv/bin/activate   # Linux/macOS
4.venv\Scripts\activate      # Windows
5.pip install -r requirements.txt
6.cd spy-cat-agency
7.python manage.py migrate
8.python manage.py runserver
```

## Main Endpoints

### Spy Cats
| Method | Endpoint | Description |
|--------|----------|------------|
| GET    | /api/spycats/ | Get all spy cats |
| POST   | /api/spycats/ | Create a new spy cat |
| PATCH  | /api/spycats/{id}/ | Update spy cat information |
| DELETE | /api/spycats/{id}/ | Delete a spy cat |

### Missions
| Method | Endpoint | Description |
|--------|----------|------------|
| GET    | /api/missions/ | Get all missions |
| POST   | /api/missions/ | Create a new mission |
| PATCH  | /api/missions/{id}/ | Update a mission |
| DELETE | /api/missions/{id}/ | Delete a mission |

### Targets
| Method | Endpoint | Description |
|--------|----------|------------|
| PATCH  | /api/targets/{id}/ | Update a target or its notes |


### Link to Postman collection:
https://maksimka0529-3463287.postman.co/workspace/%D0%9C%D0%B0%D0%BA%D1%81%D0%B8%D0%BC-%D0%9C%D0%B0%D1%86%D0%B0%D0%BF%D1%83%D1%80%D0%B0's-Workspace~84db9620-129f-4155-8af1-7097b8839baf/collection/50320962-8c69ea7f-7b38-4e79-bee4-9d21f898468b?action=share&source=copy-link&creator=50320962