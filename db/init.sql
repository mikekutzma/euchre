CREATE TABLE "users" (
  "id" uuid DEFAULT gen_random_uuid() PRIMARY KEY,
  "data" JSONB
);

