FROM node:20-alpine

WORKDIR /app

RUN corepack enable && corepack prepare pnpm@10 --activate

COPY package.json pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile

COPY . ./

EXPOSE 4321

CMD ["pnpm", "run", "dev", "--", "--host", "0.0.0.0"]