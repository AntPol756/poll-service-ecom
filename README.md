# Poll Service

Part of the **Poll System** backend (together with [user-service-ecom](https://github.com/AntPol756/user-service-ecom)).
Saves poll questions (4 options each) and the users' answers, and calculates statistics.

**Stack:** Python, FastAPI, SQLAlchemy, MySQL, Docker / Docker Compose

## Architecture

```
controllers/   HTTP layer - routes only, no logic
services/      business rules (registered users only, one answer per question, ...)
repositories/  database access (SQLAlchemy)
clients/       UserClient - calls the User Service REST API
```

### Tables (`poll_service_db`)

| questions | answers |
|---|---|
| id (PK) | id (PK) |
| title | user_id (no FK - users live in the User Service DB) |
| option_1 .. option_4 | question_id (FK -> questions.id, cascade delete) |
| | selected_option (1-4) |
| | answered_at |
| | UNIQUE (user_id, question_id) |

## Run

**Everything with Docker** (both repos cloned next to each other):

```bash
docker compose up --build
```

User Service: http://localhost:8000/docs - Poll Service: http://localhost:8001/docs

**Locally** (MySQL running on localhost:3306):

```bash
pip install -r requirements.txt
cp .env.example .env        # edit the DB password if needed
uvicorn main:app --reload --port 8001
```

The database and tables are created automatically on startup.

## Default questions

On the first start the service adds 10 example questions (see `app/seed.py`), for example:

- *Between the following, what do you most love to do?* - Watch TV / Play the computer / Hanging out with friends / Travel the world
- *Where is your preferred place to travel?* - USA / France / South America / Thailand

They are only added when the `questions` table is empty, so restarting does not create duplicates.
New questions are added with `POST /questions`.

## Answering a question

1. `GET /questions` - get the questions and their 4 options as text
2. `POST /answers` with the chosen option number (1 = first option ... 4 = fourth option)

The response also returns the question title and the chosen option as text.

## Endpoints

### Questions
| Method | Path | Notes |
|---|---|---|
| POST | `/questions` | create |
| GET | `/questions` | all questions with their options |
| GET | `/questions/{question_id}` | |
| PUT | `/questions/{question_id}` | **409** if the question already has answers |
| DELETE | `/questions/{question_id}` | also deletes its answers |

### Answers
| Method | Path | Notes |
|---|---|---|
| POST | `/answers` | `{user_id, question_id, selected_option}` - user must be registered (**403**), only once per question (**409**) |
| GET | `/answers/{answer_id}` | |
| PUT | `/answers/{answer_id}` | `{selected_option}` - change an existing answer |
| DELETE | `/answers/{answer_id}` | |
| DELETE | `/answers/user/{user_id}` | internal - called by the User Service when a user is deleted |

### Statistics
| Method | Path | Returns |
|---|---|---|
| GET | `/stats/questions/{question_id}/options` | how many users chose each option |
| GET | `/stats/questions/{question_id}/total` | how many users answered the question |
| GET | `/stats/users/{user_id}/answers` | the user's answer to each question |
| GET | `/stats/users/{user_id}/total` | how many questions the user answered |
| GET | `/stats/questions` | all questions, options and counts per option |

## Communication between services

- **Answer a question** -> Poll Service calls `GET /users/{id}` on the User Service to check the user exists and `is_registered` is true.
- **Delete a user** -> User Service calls `DELETE /answers/user/{id}` on the Poll Service.
- If the other service is down the request fails with **503** and nothing is changed.

## Testing with Postman

`postman/poll-system.postman_collection.json` tests every requirement of the project
(user CRUD, register, answer rules, statistics, deletes and cascades - 39 requests).

1. Start the system: `docker compose up --build`
2. Postman -> **Import** -> select the file
3. Collection **Poll System** -> **Run** -> run all requests in order

All tests should pass. The collection uses random emails and creates its own question,
so it can be run many times.
