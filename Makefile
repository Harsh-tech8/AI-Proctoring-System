up:
	docker compose up --build

down:
	docker compose down

logs:
	docker compose logs -f

zip:
	python scripts/generate_zip.py

clean:
	docker compose down -v
