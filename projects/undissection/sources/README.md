# Undissection source library

Retrieved and checked **11 November 2026** for private development. The initial collection supported a grades 10–12 concept; the current grades 8–10 ordinary-action prototype starts with the [school scope and curriculum grounding](school-scope.md). The [broader reading guide and accuracy cautions](reading-guide.md) retain author background, including the earlier water-and-heat direction. These are author references: the intended player learning is how structures cooperate to sustain a living whole, consistent with the repository's [philosophy](../../../README.md#philosophy).

The local library contains **25 complete OpenStax section texts**, not entire books: 101,716 whitespace-delimited words including attribution, exercises, answers, descriptions and MathML; 418 glossary definitions; and text descriptions/captions for 114 figures. Sections 9.4 and 11.1 extend the original 23-section collection for the ordinary-action prototype. Copyrighted publisher previews were inspected transiently; only bibliographic information and short original notes are retained here.

## OpenStax: edition, license and provenance

J. Gordon Betts, Kelly A. Young, James A. Wise, Eddie Johnson, Brandon Poe, Dean H. Kruse, Oksana Korol, Jody E. Johnson, Mark Womble, and Peter DeSaix. *Anatomy and Physiology 2e*. OpenStax, Rice University, Houston, 2022. [Publisher book page](https://openstax.org/details/books/anatomy-and-physiology-2e). Access for free at <https://openstax.org/books/anatomy-and-physiology-2e/pages/1-introduction>.

**The local text is the publisher's 11 March 2026 source snapshot**, commit [`b0058a743bdd2cc08196abaaa7d5469970c0d80c`](https://github.com/openstax/osbooks-anatomy-physiology/commit/b0058a743bdd2cc08196abaaa7d5469970c0d80c). That snapshot's [publisher README](https://github.com/openstax/osbooks-anatomy-physiology/blob/b0058a743bdd2cc08196abaaa7d5469970c0d80c/README.md), [LICENSE](https://github.com/openstax/osbooks-anatomy-physiology/blob/b0058a743bdd2cc08196abaaa7d5469970c0d80c/LICENSE), and [collection metadata](https://github.com/openstax/osbooks-anatomy-physiology/blob/b0058a743bdd2cc08196abaaa7d5469970c0d80c/collections/anatomy-and-physiology-2e.collection.xml) identify **Creative Commons Attribution 4.0 International**, [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Keep OpenStax/Rice University attribution, source and license links, and the transformation notice with copied material. The license excludes separately credited material and does not grant trademark rights or imply endorsement.

The current publisher website instead displays CC BY-NC-SA and an additional restriction on LLM/AI ingestion. The publisher repository records its [license change on 19 March 2026](https://github.com/openstax/osbooks-anatomy-physiology/commit/fdfa6e21ac3bc372dc2802a9952df124a619fdcc). This library therefore uses the specifically identified earlier CC BY 4.0 source, **not a full-text scrape of the current website**. The current reading links below are convenient navigation, not claims that the downloaded text matches the latest revision.

### Local files and transformations

All full-text artifacts live in [`local/openstax/`](local/openstax/) and are excluded by this directory's [`.gitignore`](.gitignore). They may be deleted after development; the index and original notes remain useful without them.

- [`original/`](local/openstax/original/) contains the downloaded original **CNXML** modules, the publisher's available historical source format. They are text, not downloaded HTML pages. Text was saved as UTF-8 with normalized line endings.
- [`markdown/`](local/openstax/markdown/) contains the complete selected section text converted to Markdown, with title, attribution, learning objectives, hierarchy, glossary, source questions and answers. Site menus and navigation were never present in these source modules.
- [`html/`](local/openstax/html/) contains **derived text-focused HTML**, not original website HTML. It provides a readable alternative for tables. No image files, video files, logos or covers were downloaded. Figure captions, credit notices and available descriptions are retained; these do not replace visual inspection when anatomy depends on a diagram.
- [`provenance/`](local/openstax/provenance/) retains the publisher license and README, collection metadata, [per-section manifest](local/openstax/provenance/manifest.json) with source URLs/checksums, and the conversion script. Tables retain HTML cell structure inside Markdown. Equations retain a linear text rendering plus their original MathML. Internal cross-references point to pinned publisher source modules; they are not local navigable figure anchors.

The conversion preserves source wording, including errors and simplified explanations. Read the [accuracy cautions](reading-guide.md#accuracy-cautions) before drafting. These files are research material, not a reviewed player script or a substitute for the book's figures.

### Selected sections in reading order

Each row links to the current publisher section and its local Markdown. The manifest connects the same row to its exact pinned source module and original CNXML.

| Section | Current publisher reading | Local Markdown | Why read it |
|---|---|---|---|
| 1.2 | [Structural Organization](https://openstax.org/books/anatomy-and-physiology-2e/pages/1-2-structural-organization-of-the-human-body) | [Read](local/openstax/markdown/1-2-structural-organization-of-the-human-body.md) | Cells, tissues, organs and systems; levels are related but distinct. |
| 1.5 | [Homeostasis](https://openstax.org/books/anatomy-and-physiology-2e/pages/1-5-homeostasis) | [Read](local/openstax/markdown/1-5-homeostasis.md) | A controlled variable, sensor, control and response. |
| 3.1 | [The Cell Membrane](https://openstax.org/books/anatomy-and-physiology-2e/pages/3-1-the-cell-membrane) | [Read](local/openstax/markdown/3-1-the-cell-membrane.md) | Selective boundaries, gradients, channels and active transport. |
| 4.1 | [Types of Tissues](https://openstax.org/books/anatomy-and-physiology-2e/pages/4-1-types-of-tissues) | [Read](local/openstax/markdown/4-1-types-of-tissues.md) | The four tissue families as recurring materials. |
| 4.2 | [Epithelial Tissue](https://openstax.org/books/anatomy-and-physiology-2e/pages/4-2-epithelial-tissue) | [Read](local/openstax/markdown/4-2-epithelial-tissue.md) | Thin exchange surfaces, selective linings and glands. |
| 4.3 | [Connective Tissue](https://openstax.org/books/anatomy-and-physiology-2e/pages/4-3-connective-tissue-supports-and-protects) | [Read](local/openstax/markdown/4-3-connective-tissue-supports-and-protects.md) | Matrix matters; bone, tendon, blood and cartilage are related. |
| 4.4 | [Muscle Tissue and Motion](https://openstax.org/books/anatomy-and-physiology-2e/pages/4-4-muscle-tissue-and-motion) | [Read](local/openstax/markdown/4-4-muscle-tissue-and-motion.md) | Skeletal, cardiac and smooth muscle have different jobs. |
| 4.5 | [Nervous Tissue](https://openstax.org/books/anatomy-and-physiology-2e/pages/4-5-nervous-tissue-mediates-perception-and-response) | [Read](local/openstax/markdown/4-5-nervous-tissue-mediates-perception-and-response.md) | Signaling cells and supporting glia. |
| 9.4 | [Synovial Joints](https://openstax.org/books/anatomy-and-physiology-2e/pages/9-4-synovial-joints) | [Read](local/openstax/markdown/9-4-synovial-joints.md) | A movable connection; read joint structure and the hinge example, without requiring the classification survey. |
| 11.1 | [Interactions of Skeletal Muscles](https://openstax.org/books/anatomy-and-physiology-2e/pages/11-1-interactions-of-skeletal-muscles-their-fascicle-arrangement-and-their-lever-systems) | [Read](local/openstax/markdown/11-1-interactions-of-skeletal-muscles-their-fascicle-arrangement-and-their-lever-systems.md) | Tendons transfer muscle pulls; opposing and assisting muscles cooperate. Skip fascicle classifications for this prototype. |
| 17.3 | [The Pituitary Gland and Hypothalamus](https://openstax.org/books/anatomy-and-physiology-2e/pages/17-3-the-pituitary-gland-and-hypothalamus) | [Read](local/openstax/markdown/17-3-the-pituitary-gland-and-hypothalamus.md) | ADH synthesis, posterior-pituitary release and osmotic feedback. |
| 19.1 | [Heart Anatomy](https://openstax.org/books/anatomy-and-physiology-2e/pages/19-1-heart-anatomy) | [Read](local/openstax/markdown/19-1-heart-anatomy.md) | Chambers, valves, walls and connected pulmonary/systemic paths. |
| 20.1 | [Blood Vessel Structure and Function](https://openstax.org/books/anatomy-and-physiology-2e/pages/20-1-structure-and-function-of-blood-vessels) | [Read](local/openstax/markdown/20-1-structure-and-function-of-blood-vessels.md) | Reused tissue layers make different kinds of vessel. |
| 20.3 | [Capillary Exchange](https://openstax.org/books/anatomy-and-physiology-2e/pages/20-3-capillary-exchange) | [Read](local/openstax/markdown/20-3-capillary-exchange.md) | Delivery across a boundary; read the Starling caution below. |
| 22.3 | [The Process of Breathing](https://openstax.org/books/anatomy-and-physiology-2e/pages/22-3-the-process-of-breathing) | [Read](local/openstax/markdown/22-3-the-process-of-breathing.md) | Pressure differences, respiratory muscles and ventilation control. |
| 22.4 | [Gas Exchange](https://openstax.org/books/anatomy-and-physiology-2e/pages/22-4-gas-exchange) | [Read](local/openstax/markdown/22-4-gas-exchange.md) | Diffusion, partial pressures, thin surfaces and matching flow. |
| 22.5 | [Transport of Gases](https://openstax.org/books/anatomy-and-physiology-2e/pages/22-5-transport-of-gases) | [Read](local/openstax/markdown/22-5-transport-of-gases.md) | Hemoglobin carries oxygen; much carbon dioxide travels as bicarbonate. |
| 23.7 | [Chemical Digestion and Absorption](https://openstax.org/books/anatomy-and-physiology-2e/pages/23-7-chemical-digestion-and-absorption-a-closer-look) | [Read](local/openstax/markdown/23-7-chemical-digestion-and-absorption-a-closer-look.md) | Food breakdown and selective uptake are separate processes. |
| 24.1 | [Overview of Metabolic Reactions](https://openstax.org/books/anatomy-and-physiology-2e/pages/24-1-overview-of-metabolic-reactions) | [Read](local/openstax/markdown/24-1-overview-of-metabolic-reactions.md) | Catabolism, anabolism, enzymes and ATP. |
| 24.2 | [Carbohydrate Metabolism](https://openstax.org/books/anatomy-and-physiology-2e/pages/24-2-carbohydrate-metabolism) | [Read](local/openstax/markdown/24-2-carbohydrate-metabolism.md) | How nutrient processing supports cellular work; read corrections below. |
| 24.6 | [Energy and Heat Balance](https://openstax.org/books/anatomy-and-physiology-2e/pages/24-6-energy-and-heat-balance) | [Read](local/openstax/markdown/24-6-energy-and-heat-balance.md) | Heat regulation and cooling through sweat evaporation. |
| 25.4 | [Microscopic Anatomy of the Kidney](https://openstax.org/books/anatomy-and-physiology-2e/pages/25-4-microscopic-anatomy-of-the-kidney) | [Read](local/openstax/markdown/25-4-microscopic-anatomy-of-the-kidney.md) | The nephron has connected blood and tubular compartments. |
| 25.5 | [Physiology of Urine Formation](https://openstax.org/books/anatomy-and-physiology-2e/pages/25-5-physiology-of-urine-formation) | [Read](local/openstax/markdown/25-5-physiology-of-urine-formation.md) | Filtration is selective and pressure-dependent. |
| 25.6 | [Tubular Reabsorption](https://openstax.org/books/anatomy-and-physiology-2e/pages/25-6-tubular-reabsorption) | [Read](local/openstax/markdown/25-6-tubular-reabsorption.md) | Recovery, secretion, gradients and adjustable water retention. |
| 26.2 | [Water Balance](https://openstax.org/books/anatomy-and-physiology-2e/pages/26-2-water-balance) | [Read](local/openstax/markdown/26-2-water-balance.md) | Hypothalamic sensing, thirst, ADH and water conservation. |

For the earlier water-and-heat prototype, [the focused mechanism notes](reading-guide.md#water-and-heat-prototype) preserve its source interpretation. Sections 17.3 and 26.2 supply the hypothalamic-sensing/ADH loop; 25.6 supplies the collecting-duct permeability and medullary-gradient relationship; 23.7 supplies intestinal absorption. Those mechanisms are outside the current [school scope](school-scope.md).

## Copyrighted references: links and original notes only

### Silverthorn: integrated physiology

Dee Unglaub Silverthorn. *Human Physiology: An Integrated Approach*, 7th edition. Pearson. Student ISBN 978-0-321-98122-6. The official [24-page front matter/preface preview](https://www.pearsoncanada.ca/media/highered-showcase/multi-product-showcase/silverthorn-preface.pdf) was readable through web extraction. Its contents make integration explicit: cellular processes and communication support later work on circulation, breathing, kidneys, metabolism and exercise.

The official [chapter 21 sample, The Digestive System](https://www.pearson.com/content/dam/one-dot-com/one-dot-com/us/en/higher-ed/en/products-services/silverthorn-7e-info/pdf/sample-chapter--ch21.pdf) was actually retrieved (HTTP 200; 39 PDF pages) and text-extracted in memory after the web reader rejected its size. No PDF or full extracted text was retained. It distinguishes motility, secretion, digestion and absorption, then examines coordinated control across digestive phases. **Design inference:** a useful organ assembly should connect a physical structure to several cooperating processes, including a trigger and a response; attaching an organ label is insufficient.

Coverage is these two previews, not the full textbook, later editions or its ancillary resources. No open reproduction license was established.

### Sherwood: homeostasis across systems

Lauralee Sherwood. *Human Physiology: From Cells to Systems*, 9th edition, © 2016. Cengage. ISBN 9781285866932. The [official publisher page](https://www.cengage.com/c/human-physiology-from-cells-to-systems-9e-sherwood/9781285866932) was accessed; its description and contents explicitly connect mechanisms, structural organization, internal environment and homeostatic control. Chapter material itself was not downloaded or converted.

**Design inference:** revisit a shared controlled condition as each organ becomes available. Circulation can distribute substances, but stable internal conditions also require exchange surfaces, usable nutrients, waste routes and adjustment mechanisms. Treat homeostasis as the reason the assembled parts matter, not as a detached final vocabulary lesson. No open reproduction license was established.

### Zahourek: constructive anatomy

Jon Zahourek. *Basic Muscles, Nerves & Blood Vessels of the Human Arm*, The StepByStep™ Series, Anatomy In Clay® Publications, a division of Zahourek Systems, Inc. The [supplied workbook PDF](https://www.coolscience.org/uploads/1/0/7/7/107782681/stepbystep%E2%84%A2_human_arm.pdf) was actually retrieved (HTTP 200; 46 PDF pages) and text-extracted in memory. Its cover carries 2010–2013 and the copyright page 2010–2015. The copyright notice reserves rights; no persistent PDF, full text, images or modeled shapes were kept.

**Design inference:** constructive anatomy offers a spatial counterpart to dissection: each addition should reveal how neighboring structures fit and cooperate. This arm workbook is a precedent for building anatomical relationships, not evidence that the proposed digital game improves learning, and not a source for reproducing its proprietary models or artwork.

### Spongelab: access not established

The supplied [Build-a-Body address](https://www.spongelab.com/game_pages/BAB.cfm) was **not successfully accessed**. On the retrieval date the web reader reported HTTP 502; a separate direct request failed DNS resolution. This establishes only failure of these attempts, not global or permanent unavailability. No live gameplay, screenshots, content or educational claims from this page were verified or retained.

## Coverage limits

This is a focused mechanism library, not a complete high-school biology syllabus or full human anatomy collection. It does not systematically cover reproductive development, immunity, sensory systems, musculoskeletal detail, disease, clinical treatment or every endocrine loop. It has no learning-effectiveness study of the proposed game. The OpenStax material is college introductory level; the [school scope](school-scope.md) selects the current grades 8–10 teaching boundary. A story about assembling a model must not imply that mature organs are manufactured by simply sticking generic tissues together in real embryological development.
