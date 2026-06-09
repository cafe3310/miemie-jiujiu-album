---
name: chocho-miemie-gallery
description: A stark visual gallery showcasing cat-themed art and diaries.
colors:
  primary: "#1a1a1a"
  neutral-bg: "#ffffff"
  neutral-border: "#eaeaea"
  neutral-text-muted: "#888888"
  neutral-surface: "#fafafa"
typography:
  display:
    fontFamily: "Inter, system-ui, Avenir, Helvetica, Arial, sans-serif"
    fontSize: "2.2rem"
    fontWeight: 300
    lineHeight: 1.6
    letterSpacing: "-0.03em"
  headline:
    fontFamily: "Inter, system-ui, Avenir, Helvetica, Arial, sans-serif"
    fontSize: "1.35rem"
    fontWeight: 400
    lineHeight: 1.6
    letterSpacing: "-0.01em"
  body:
    fontFamily: "Inter, system-ui, Avenir, Helvetica, Arial, sans-serif"
    fontSize: "0.95rem"
    fontWeight: 400
    lineHeight: 1.6
  label:
    fontFamily: "ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace"
    fontSize: "0.85rem"
    fontWeight: 400
    lineHeight: 1.5
rounded:
  none: "0px"
  sm: "4px"
spacing:
  sm: "8px"
  md: "16px"
  lg: "24px"
components:
  button-primary:
    textColor: "{colors.primary}"
    backgroundColor: "{colors.neutral-bg}"
    rounded: "{rounded.none}"
  link-card:
    rounded: "{rounded.none}"
    padding: "20px 24px"
  gallery-item:
    rounded: "{rounded.none}"
    backgroundColor: "{colors.neutral-surface}"
---

# Design System: chocho-miemie-gallery

## 1. Overview

**Creative North Star: "The Monochromatic Gallery: A stark, high-contrast canvas where content acts as the sole color, and space provides the rhythm."**

This design system is crafted to project a quiet, minimalist editorial environment. By removing decorative accents, shadows, and motion, the layout operates as a clean paper gallery where the cat photos and generated illustrations serve as the exclusive focus of color and expression.

Visual structure is established through scale hierarchy, generous whitespace, and sharp edges. It explicitly rejects conventional SaaS styling elements, opting instead for structural quietness.

**Key Characteristics:**
- **Content-first hierarchy**: Layout elements are silent, framing rather than distracting from the media.
- **Purely static interaction**: Total elimination of transitions and animations to ensure low friction and instant feedback.
- **Stark geometry**: Hard sharp corners (0px) and clean grid dividers.

## 2. Colors

The color palette is restricted to a high-contrast ink-on-paper scheme, reserving chroma exclusively for content.

### Primary
- **Stark Charcoal** (#1a1a1a): Applied to primary headings, active navigational text, and main visual highlights.

### Neutral
- **Bright White** (#ffffff): The main canvas background, establishing massive negative space.
- **Off-White Surface** (#fafafa): A light backing tint for code blocks and media placeholders.
- **Soft Ash** (#eaeaea): The thin dividing border color for structure and visual grouping.
- **Muted Grey** (#888888): Reserved for metadata, subtitles, inactive states, and captions.

### Named Rules
**The Colorless Canvas Rule.** No background color or text highlight color other than neutrals (#ffffff, #fafafa, #1a1a1a) is permitted. Chroma is reserved strictly for images and video assets.

## 3. Typography

**Display Font:** Inter, system-ui (sans-serif)
**Body Font:** Inter, system-ui (sans-serif)
**Label/Mono Font:** ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas (monospace)

### Hierarchy
- **Display** (300, 2.2rem, 1.6): Used for main site branding titles in the header.
- **Headline** (400, 1.35rem, 1.6): Used for post titles and gallery section headers.
- **Body** (400, 0.95rem, 1.6): Used for descriptions, prose, and summaries. Maximum line length is capped at 75ch.
- **Label** (400, 0.85rem, 1.5): Used for monospaced parameters, metadata labels, and captions.

## 4. Elevation

Depth is expressed solely through thin borders and flat surface layering rather than shadows. The page feels entirely flat, physical, and print-like.

### Named Rules
**The Hard Edge Rule.** All borders, boxes, and interactive cards must use a border-radius of 0px. Sharp geometric boundaries define the editorial structure.
**The No-Shadow Rule.** Depth shadows (box-shadow or text-shadow) are strictly prohibited, keeping all elements flat at rest.

## 5. Components

Components are styled with minimal footprint, emphasizing flat shapes and instant hover swaps.

### Buttons
- **Shape:** Sharp sharp corners (0px).
- **Navigation Links:** Inline layout with standard underline styles.
- **Hover / Focus:** Changes color instantly from Muted Grey (#888888) to Stark Charcoal (#1a1a1a) on hover.

### Cards / Containers
- **Corner Style:** Sharp sharp corners (0px).
- **Background:** White (#ffffff) or flat Off-White Surface (#fafafa).
- **Border:** Thin solid Soft Ash (1px solid #eaeaea) or light grey (#eeeeee).
- **Internal Padding:** Standard 20px-24px padding bounds.

### Gallery Items
- **Corner Style:** Sharp sharp corners (0px).
- **Background:** Off-White Surface (#fafafa).
- **Border:** Thin borders that change color from Soft Ash to Stark Charcoal instantly on hover, without transition durations.

## 6. Do's and Don'ts

Concrete guidelines to enforce the editorial aesthetic.

### Do:
- **Do** align structural divisions to a clean, grid-based grid with 1px border lines.
- **Do** wrap code elements in sharp-cornered light grey blocks.
- **Do** use large whitespace margins (such as 4rem to 5rem) to separate site branding from list cards.

### Don't:
- **Don't** use side-stripe borders greater than 1px as an accent highlight.
- **Don't** apply any CSS transitions (`transition` property) or animation keyframes.
- **Don't** use rounded corners (`border-radius`) except for external/default code highlights.
- **Don't** use SaaS template layouts featuring multi-column dashboards or icon grids.
