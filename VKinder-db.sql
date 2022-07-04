CREATE TABLE "city" (
  "id" SERIAL PRIMARY KEY,
  "title" varchar(60) NOT NULL
);

CREATE TABLE "ages" (
  "id" SERIAL PRIMARY KEY,
  "value" integer NOT NULL
);

CREATE TABLE "sex" (
  "id" SERIAL PRIMARY KEY,
  "title" varchar(60) NOT NULL
);

CREATE TABLE "userinfo" (
  "id" SERIAL PRIMARY KEY,
  "user_name" varchar(60) UNIQUE NOT NULL,
  "vk_id" varchar(60) UNIQUE NOT NULL,
  "vk_link" varchar(60) UNIQUE NOT NULL,
  "city_id" integer,
  "age_id" integer,
  "sex_id" integer
);

CREATE TABLE "_match" (
  "id" SERIAL PRIMARY KEY,
  "match_name" varchar(60) UNIQUE NOT NULL,
  "vk_id" varchar(60) UNIQUE NOT NULL,
  "vk_link" varchar(60) UNIQUE NOT NULL,
  "city_id" integer,
  "age_id" integer,
  "sex_id" integer
);

CREATE TABLE "user_match" (
  "user_id" integer,
  "match_id" integer,
  PRIMARY KEY ("user_id", "match_id")
);

ALTER TABLE "userinfo" ADD FOREIGN KEY ("city_id") REFERENCES "city" ("id");

ALTER TABLE "userinfo" ADD FOREIGN KEY ("age_id") REFERENCES "ages" ("id");

ALTER TABLE "userinfo" ADD FOREIGN KEY ("sex_id") REFERENCES "sex" ("id");

ALTER TABLE "_match" ADD FOREIGN KEY ("city_id") REFERENCES "city" ("id");

ALTER TABLE "_match" ADD FOREIGN KEY ("age_id") REFERENCES "ages" ("id");

ALTER TABLE "_match" ADD FOREIGN KEY ("sex_id") REFERENCES "sex" ("id");

ALTER TABLE "user_match" ADD FOREIGN KEY ("user_id") REFERENCES "userinfo" ("id");

ALTER TABLE "user_match" ADD FOREIGN KEY ("match_id") REFERENCES "_match" ("id");
