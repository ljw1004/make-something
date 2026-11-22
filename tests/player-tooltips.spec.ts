import { expect, test } from '@playwright/test';

test('ordinary item hover uses highlighting without a native drag tooltip', async ({page}) => {
  const manuscript = `# Tooltip fixture
## Workshop
Make a kit.

**Goals**
- Build -- Kit
**Items**
- Frame
- Tool

  Tool explanation.

- Kit
**Combinations**
- Frame [preserve] + Tool [preserve] -> Kit
`;
  await page.route('**/tooltip-fixture.md', route =>
    route.fulfill({contentType:'text/markdown',body:manuscript}));
  await page.goto('/index.html?story=tooltip-fixture.md');
  await page.getByRole('button',{name:'Start',exact:true}).click();
  await page.getByRole('button',{name:'Begin',exact:true}).click();
  const frame = page.locator('[data-item="name:Frame"]');
  await frame.hover();
  expect(await frame.getAttribute('title')).toBeNull();
  await expect(frame).toHaveAccessibleName('Frame');
  await expect(frame).toHaveClass(/\bpressed\b/);
  await expect(page.locator('[data-item="name:Tool"]')).toHaveClass(/\bpossible\b/);
  await expect(page.locator('[data-item="name:Tool"]')).toHaveAttribute('title','Double-click or double-tap to read');
});
