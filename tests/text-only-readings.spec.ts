import {test,expect} from '@playwright/test';
import {openDebugPanel} from './debug-helpers.ts';

test('text-only item passages never show blank popups or empty reading controls, including reload',async({page})=>{
 const source=`# Visual captions
## Build
**Goals**
- Make C -- C
- next: Finish -- D
**Items**
- A
  {A flat red square.}
- B
- C
  {A red square with one folded corner.}
- Part
- D
  Finished. {A red square with two folded corners.}
  ---
  {Two corners are folded.}
  Read the [source](https://example.com).
**Combinations**
- A [transform] + B [consume] -> C
- C [transform] + Part [consume] -> D
`;
 await page.route('**/text-caption-fixture.md',route=>route.fulfill({contentType:'text/markdown',body:source}));
 await page.goto('/make-something.html?story=text-caption-fixture.md');
 await page.getByRole('button',{name:'Start',exact:true}).click();
 await expect(page.locator('[data-item="name:A"] .reading-indicator')).toHaveCount(0);
 await page.locator('[data-item="name:A"]').dblclick();await expect(page.getByRole('dialog')).toHaveCount(0);
 await page.locator('[data-item="name:A"]').dragTo(page.locator('[data-item="name:B"]'));
 await expect(page.locator('[data-item="name:C"]')).toBeVisible();
 await expect(page.getByRole('dialog')).toHaveCount(0);
 await expect(page.locator('[data-item="name:C"] .reading-indicator')).toHaveCount(0);
 await page.reload();await expect(page.locator('[data-item="name:C"]')).toBeVisible();
 await expect(page.getByRole('dialog')).toHaveCount(0);
 await page.locator('[data-item="name:C"]').dragTo(page.locator('[data-item="name:Part"]'));
 await expect(page.locator('dialog.wonder .reading-text')).toHaveText('Finished.');
 await page.getByRole('button',{name:'Continue',exact:true}).click();
 await page.locator('[data-item="name:D"]').dblclick();
 await expect(page.locator('.encyclopedia-reading')).toHaveText('Read the source.');
 await expect(page.locator('.encyclopedia-reading a')).toHaveAttribute('href','https://example.com');
 await expect(page.locator('.encyclopedia-list a')).toHaveText(['D']);
});

test('live edits can hide and restore a pending reading without losing the construction or editor focus',async({page})=>{
 await page.setViewportSize({width:1280,height:800});
 const source=`# Editable captions
## Build
**Goals**
- Finish -- C
**Items**
- A
- B
- C
  Visible result.
**Combinations**
- A [transform] + B [consume] -> C
`;
 await page.route('**/editable-caption-fixture.md',route=>route.fulfill({contentType:'text/markdown',body:source}));
 await page.goto('/make-something.html?story=editable-caption-fixture.md');
 await page.getByRole('button',{name:'Start',exact:true}).click();
 await openDebugPanel(page);
 await page.locator('[data-item="name:A"]').dragTo(page.locator('[data-item="name:B"]'));
 await expect(page.locator('dialog.wonder .reading-text')).toHaveText('Visible result.');
 const editor=page.getByRole('textbox',{name:'Story Markdown'});
 const replace=async(text:string)=>{await editor.focus();await page.keyboard.press('ControlOrMeta+A');await page.keyboard.insertText(text);};
 await replace(source.replace('Visible result.','{A red square with a folded corner.}'));
 await expect(page.getByRole('dialog')).toHaveCount(0);
 await expect(editor).toBeFocused();
 await expect(page.locator('[data-item="name:C"]')).toBeVisible();
 await replace(source);
 await expect(page.locator('dialog.wonder .reading-text')).toHaveText('Visible result.');
 await expect(editor).toBeFocused();
 await page.getByRole('button',{name:'Continue',exact:true}).click();
 await page.reload();
 await expect(page.locator('[data-item="name:C"]')).toBeVisible();
 await expect(page.getByRole('dialog')).toHaveCount(0);
});
