
CREATE TABLE "production" (
	"id" serial NOT NULL,
	"product" varchar(255),
	"year" timestamp,
	"category" varchar(255),
	"quantity" float,
	PRIMARY KEY("id")
);

/**
KG
*/
CREATE TABLE "processing" (
	"id" serial NOT NULL,
	"product" varchar(255),
	"value" float,
	"year" date,
	"category" varchar(255),
	"control" varchar(255),
	PRIMARY KEY("id")
);

CREATE TABLE "commercialization" (
	"id" serial NOT NULL,
	"product" varchar(255),
	"year" timestamp,
	"category" varchar(255),
	"value" float,
	"control" varchar(255),
	PRIMARY KEY("id")
);

CREATE TABLE "exporting" (
	"id" serial NOT NULL,
	"country" varchar(255),
	"year" timestamp,
	"value" float,
	PRIMARY KEY("id")
);

CREATE TABLE "importing" (
	"id" serial NOT NULL,
	"country" varchar(255),
	"year" timestamp,
	"value" float,
	PRIMARY KEY("id")
);
