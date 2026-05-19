FROM node:22.12-alpine AS build

WORKDIR /app

RUN npm install -g pnpm@10.17.1

COPY package.json pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile

COPY . ./

RUN pnpm build

FROM python:3.12-slim

WORKDIR /app

COPY --from=build /app/dist ./dist
COPY server.py ./server.py

EXPOSE 4321

ENV PORT=4321
ENV BACKEND_URL=http://backend:8000

CMD ["python", "server.py"]