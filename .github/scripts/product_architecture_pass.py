from pathlib import Path

root=Path(__file__).resolve().parents[2]

# Correct chapter slugs against the canonical theory corpus.
product=root/'web/src/cem-product-map.ts'
s=product.read_text()
s=s.replace("chapterSlug:'editorial-selection'","chapterSlug:'editorial-selection-observed-world'")
s=s.replace("chapterSlug:'presentation-framing-congruence'","chapterSlug:'framing-congruence'")
product.write_text(s)

# New persistent disclosures must remain real interaction targets in every contextual surface.
css=root/'web/src/suite-overview.css'
c=css.read_text()
c=c.replace('.suite-learning-more summary{min-height:44px;display:flex;align-items:center;cursor:pointer}', '.suite-learning-more>summary{display:block;width:100%;min-width:24px;min-height:44px;cursor:pointer;overflow-wrap:anywhere}')
c=c.replace('.suite-more-diagnostics>summary{min-height:44px;display:flex;align-items:center;cursor:pointer}', '.suite-more-diagnostics>summary{display:block;width:100%;min-width:24px;min-height:44px;cursor:pointer;overflow-wrap:anywhere}')
css.write_text(c)

# Connect the shared four-region shell to a persistent contextual CEM focus.
main=root/'web/src/main.ts'
s=main.read_text()
old="let contextualTool:'search'|'inspector'|null=null;"
new=old+"\nlet suiteFocus='overview';"
if old not in s:
    raise SystemExit('main contextualTool anchor missing')
s=s.replace(old,new,1)
old_version='<a class="version" id="releaseVersion" href="https://github.com/LaurentiuStaicu/cognitive-epistemic-model/releases/tag/${release.release_tag}" target="_blank" rel="noopener">${release.channel} ${release.version} · ${release.model}</a>'
new_purpose='<span class="product-purpose">${tr(\'Explorează cum informația devine judecată și acțiune\',\'Explore how information becomes judgment and action\')}</span>'
if old_version not in s:
    raise SystemExit('main release badge anchor missing')
s=s.replace(old_version,new_purpose,1)
old_footer="<footer><span>${tr('Model demonstrativ · coeficienți necalibrați','Demonstration model · uncalibrated coefficients')}</span><span>${tr('Calibrarea rămâne dormantă până după v1 · web-first','Calibration remains dormant until after v1 · web-first')}</span></footer>"
new_footer="<footer><span>${tr('Prototip de cercetare orientat spre dovezi · coeficienți populaționali necalibrați','Evidence-aware research prototype · uncalibrated population coefficients')}</span><span>EMPIRICAL · EXECUTABLE · CONCEPTUAL · INTERPRETIVE</span></footer>"
if old_footer not in s:
    raise SystemExit('main footer anchor missing')
s=s.replace(old_footer,new_footer,1)
old_mount=" const openTool=(tool:'search'|'inspector')=>{stop();view='learning';contextualTool=tool;shell();};\n mountSuiteOverview(suiteRoot,{lang,softwareVersion:release.version,modelSpecification:release.model,variableCount:variables.length,moduleCount:modules.length,referenceCount:references.length,validationCount:validationTests.length,openUnderstanding,openView:openSuiteView,openTool});"
new_mount=""" const openTool=(tool:'search'|'inspector')=>{stop();view='learning';contextualTool=tool;shell();};
 const openFocus=(id:string)=>{stop();suiteFocus=id;contextualTool=null;shell();requestAnimationFrame(()=>{const target=id==='overview'?'available-information':id;document.querySelector<HTMLButtonElement>(`[data-suite-focus=\"${CSS.escape(target)}\"]`)?.focus({preventScroll:false});});};
 const openTheoryChapter=(slug:string)=>{stop();view='learning';contextualTool=null;localStorage.setItem('cem-understanding-mode','theory');const target=`#understanding/theory/${slug}`;if(location.hash===target)shell();else location.hash=target;};
 const openReference=(id:string)=>{stop();view='reference';registryFocus=id;contextualTool=null;if(location.hash.startsWith('#understanding/'))history.replaceState(null,'',location.pathname+location.search);shell();};
 mountSuiteOverview(suiteRoot,{lang,selectedFocus:suiteFocus,openFocus,openUnderstanding,openTheoryChapter,openReference,openView:openSuiteView,openTool});"""
if old_mount not in s:
    raise SystemExit('main suite mount anchor missing')
s=s.replace(old_mount,new_mount,1)
main.write_text(s)

# Browser contract: a new user must be able to understand and traverse the product from the page itself.
smoke=root/'web/scripts/smoke.mjs'
s=smoke.read_text()
old=""" assert.equal(await page.locator('.suite-aux-panel').count(),1);
 assert.equal(await page.locator('input[type=\\\"file\\\"]').count(),0);
 await page.locator('#language').click();"""
new=""" assert.equal(await page.locator('.suite-aux-panel').count(),1);
 assert.equal(await page.locator('.cem-system-node').count(),20);
 assert.equal(await page.locator('.cem-system-edge').count(),23);
 assert.equal(await page.locator('.suite-dashboard-panel').getByText('Version',{exact:true}).count(),0);
 assert.equal(await page.locator('#releaseVersion').count(),0);
 assert.equal(await page.locator('input[type=\\\"file\\\"]').count(),0);
 await page.locator('[data-suite-focus=\\\"familiarity\\\"]').click();
 assert.equal(await page.locator('[data-suite-focus=\\\"familiarity\\\"]').getAttribute('aria-pressed'),'true');
 assert((await page.locator('.cem-system-edge.is-related').count())>=2);
 assert.match(await page.locator('.suite-theory-panel').textContent(),/Familiarity/);
 assert.match(await page.locator('.suite-aux-panel').textContent(),/Provenance/);
 assert((await page.locator('[data-suite-reference]').count())>=2);
 await page.locator('[data-suite-theory-chapter]').click();
 await page.waitForURL(/#understanding\\/theory\\/repetition-familiarity-truth$/);
 await waitTheory();
 assert.match(await page.locator('#suiteTheoryContext #theoryArticle:visible').textContent(),/Repetition, familiarity and judged truth/);
 await page.locator('#language').click();"""
if old not in s:
    raise SystemExit('smoke primary shell anchor missing')
s=s.replace(old,new,1)
old_version_block=""" const version=JSON.parse(await readFile(path.join(dist,'model/version.json'),'utf8'));
 assert.match(await page.locator('#releaseVersion').textContent(),new RegExp(version.version.replaceAll('.', '\\\\.')));
 assert((await page.locator('#releaseVersion').getAttribute('href')).endsWith('/'+version.release_tag));
"""
if old_version_block not in s:
    raise SystemExit('smoke releaseVersion block missing')
s=s.replace(old_version_block,"",1)
smoke.write_text(s)
