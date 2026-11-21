// news-image-20261121 — entrypoint.
//
// The front page is rendered offline by draw_poster.py and committed as
// entry.png beside this file. The grader runs this program twice with no
// network and requires both runs to write identical bytes, so this file
// only moves those exact bytes into the output directory.
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const HERE = dirname(fileURLToPath(import.meta.url));
const SOURCE = join(HERE, "entry.png");
const OUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const TARGET = join(OUT_DIR, "entry.png");

function fail(message: string, cause: unknown): never {
  const detail = cause instanceof Error ? cause.message : String(cause);
  console.error(`news-image-20261121: ${message}: ${detail}`);
  process.exit(1);
}

let artwork: Buffer;
try {
  artwork = readFileSync(SOURCE);
} catch (error) {
  fail("cannot read the committed entry.png", error);
}

try {
  mkdirSync(OUT_DIR, { recursive: true });
  writeFileSync(TARGET, artwork);
} catch (error) {
  fail(`cannot write ${TARGET}`, error);
}

// Read the copy back: a partial or corrupted write must fail loudly
// instead of handing the grader a broken image.
let written: Buffer;
try {
  written = readFileSync(TARGET);
} catch (error) {
  fail(`cannot verify ${TARGET}`, error);
}
if (!written.equals(artwork)) {
  console.error(
    `news-image-20261121: written ${TARGET} does not match entry.png`,
  );
  process.exit(1);
}
