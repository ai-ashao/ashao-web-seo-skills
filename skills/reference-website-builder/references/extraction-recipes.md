# Deterministic extraction recipes

Use these recipes only when high-fidelity reconstruction is active. They standardize what gets measured so builders do not receive incomplete, impressionistic briefs.

The scripts are inspection helpers, not production code. Run them through an authorized browser automation context on the explicit in-scope page.

## 1. Component computed-style capture

Choose a stable component root selector. Prefer a bounded root such as a section, card, toolbar, workbench panel, or navigation region.

The following recipe captures a fixed property set and walks a limited descendant depth. Adjust the selector and depth when necessary; do not indiscriminately serialize the entire page.

```js
(function captureComponent(selector, maxDepth = 4) {
  const root = document.querySelector(selector);
  if (!root) return JSON.stringify({ error: `missing: ${selector}` });

  const props = [
    'fontSize','fontWeight','fontFamily','lineHeight','letterSpacing','color',
    'textTransform','textDecoration',
    'backgroundColor','background','backgroundImage',
    'padding','paddingTop','paddingRight','paddingBottom','paddingLeft',
    'margin','marginTop','marginRight','marginBottom','marginLeft',
    'width','height','maxWidth','minWidth','maxHeight','minHeight','aspectRatio',
    'display','flexDirection','flexWrap','justifyContent','alignItems','alignContent','gap',
    'gridTemplateColumns','gridTemplateRows','gridAutoFlow','order',
    'borderRadius','border','borderTop','borderRight','borderBottom','borderLeft',
    'boxShadow','overflow','overflowX','overflowY',
    'position','top','right','bottom','left','inset','zIndex',
    'opacity','transform','transformOrigin','transition','animation',
    'cursor','pointerEvents',
    'objectFit','objectPosition','mixBlendMode','filter','backdropFilter',
    'whiteSpace','textOverflow','WebkitLineClamp'
  ];

  const meaningful = value =>
    value && value !== 'normal' && value !== 'none' && value !== 'auto' &&
    value !== '0px' && value !== 'rgba(0, 0, 0, 0)';

  function styles(el) {
    const cs = getComputedStyle(el);
    return Object.fromEntries(
      props.map(p => [p, cs[p]]).filter(([, v]) => meaningful(v))
    );
  }

  function walk(el, depth) {
    if (depth > maxDepth) return null;
    const children = [...el.children];
    const directText = [...el.childNodes]
      .filter(n => n.nodeType === Node.TEXT_NODE)
      .map(n => n.textContent.trim())
      .filter(Boolean)
      .join(' ')
      .slice(0, 240);

    return {
      tag: el.tagName.toLowerCase(),
      id: el.id || null,
      classes: typeof el.className === 'string'
        ? el.className.split(/\s+/).filter(Boolean).slice(0, 8)
        : [],
      text: directText || null,
      styles: styles(el),
      media: el.tagName === 'IMG'
        ? { src: el.currentSrc || el.src, alt: el.alt, naturalWidth: el.naturalWidth, naturalHeight: el.naturalHeight }
        : null,
      childCount: children.length,
      children: children.slice(0, 24).map(c => walk(c, depth + 1)).filter(Boolean)
    };
  }

  return JSON.stringify(walk(root, 0), null, 2);
})('SELECTOR');
```

Record the selector, viewport, scroll position, state, and timestamp/context beside the output.

## 2. Page asset discovery

Run once per explicit page and again after switching major stateful panels when their media changes.

```js
JSON.stringify({
  images: [...document.querySelectorAll('img')].map(img => ({
    src: img.currentSrc || img.src,
    alt: img.alt,
    naturalWidth: img.naturalWidth,
    naturalHeight: img.naturalHeight,
    rendered: { width: img.getBoundingClientRect().width, height: img.getBoundingClientRect().height },
    position: getComputedStyle(img).position,
    zIndex: getComputedStyle(img).zIndex,
    parentClass: typeof img.parentElement?.className === 'string' ? img.parentElement.className : '',
    siblingImages: img.parentElement ? img.parentElement.querySelectorAll('img').length : 0
  })),
  pictures: [...document.querySelectorAll('picture')].map(p => ({
    sources: [...p.querySelectorAll('source')].map(s => ({ srcset: s.srcset, media: s.media, type: s.type })),
    img: p.querySelector('img')?.currentSrc || p.querySelector('img')?.src || null
  })),
  videos: [...document.querySelectorAll('video')].map(v => ({
    src: v.currentSrc || v.src || v.querySelector('source')?.src || null,
    poster: v.poster || null,
    autoplay: v.autoplay,
    loop: v.loop,
    muted: v.muted,
    playsInline: v.playsInline
  })),
  backgrounds: [...document.querySelectorAll('*')]
    .map(el => ({ el, bg: getComputedStyle(el).backgroundImage }))
    .filter(x => x.bg && x.bg !== 'none')
    .slice(0, 500)
    .map(x => ({
      element: `${x.el.tagName.toLowerCase()}#${x.el.id || ''}.${typeof x.el.className === 'string' ? x.el.className.split(/\s+/)[0] || '' : ''}`,
      backgroundImage: x.bg
    })),
  inlineSvgCount: document.querySelectorAll('svg').length,
  favicons: [...document.querySelectorAll('link[rel*="icon"]')].map(l => ({ href: l.href, sizes: String(l.sizes || '') })),
  fontFamilies: [...new Set(
    [...document.querySelectorAll('body *')].slice(0, 250).map(el => getComputedStyle(el).fontFamily)
  )]
}, null, 2);
```

Use this inventory to identify layered compositions. A visually single "hero image" may actually be background + product screenshot + overlay + badge + foreground icon.

## 3. Interaction-state capture

For any stateful component:

1. capture state A with the component recipe;
2. trigger exactly one interaction through the browser tool;
3. capture state B using the same selector and viewport;
4. record the property/content differences;
5. record the trigger mechanism and transition.

Use this form:

```text
Trigger:
Viewport / scroll position:
State A:
State B:
Changed properties/content:
Transition:
Observed mechanism:
Confidence: observed / inferred / unknown
```

For scroll-driven behavior, scroll slowly before clicking. Determine whether the real driver is scroll position, intersection, sticky layout, CSS scroll animation, or a click handler.

## 4. Responsive capture

At minimum for high-fidelity work:

- desktop: approximately 1440 CSS px;
- tablet: approximately 768 CSS px when the page materially changes;
- mobile: approximately 390 CSS px.

Capture the same component at equivalent content/state where possible. Record actual topology changes rather than assuming framework breakpoints.

## 5. Builder evidence packet

Before a builder receives a component, assemble:

- component spec;
- target file;
- screenshot/evidence path;
- measured style excerpt;
- interaction-state differences;
- responsive rules;
- logical asset IDs;
- integration constraints;
- acceptance criteria.

If a worker still has to guess a material value or interaction model, extraction is incomplete.
