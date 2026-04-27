import re

with open('index_premium.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update image src and style
old_img = r'<img src="images/digital_guide_v2_nobg\.png" alt="Premium" style="background:var\(--beige-chip\); padding:2px; border:1px solid var\(--amber-gold\); object-fit:contain; border-radius:50%; width:40px; height:40px;">'
new_img = r'<img src="images/livro_icone.png" alt="Protocolo" style="background:var(--beige-chip); padding:4px; border:1px solid var(--amber-gold); object-fit:contain; border-radius:6px; width:44px; height:44px;">'

html = re.sub(old_img, new_img, html)

# 2. Update JS Logic
js_target = r'''  const names = \["Maria C\. \(SP\)", "Sônia R\. \(RJ\)", "Lúcia T\. \(MG\)", "Aparecida M\. \(RS\)", "Helena S\. \(PR\)", "Fátima V\. \(SC\)", "Neuza B\. \(GO\)"\];
  if\(socialToast\) \{
    function showToast\(\) \{
      stName\.innerHTML = <strong>\$\{names\[Math\.floor\(Math\.random\(\)\*names\.length\)\]\}<\/strong>;
      socialToast\.classList\.add\('show'\);
      if \(navigator\.vibrate\) \{ try\{ navigator\.vibrate\(\[30, 50, 30\]\); \} catch\(e\)\{\} \}
      setTimeout\(\(\) => \{ 
        socialToast\.classList\.remove\('show'\); 
        setTimeout\(showToast, Math\.floor\(Math\.random\(\) \* 25000\) \+ 12000\); // 12s to 37s
      \}, 6000\);
    \}
    setTimeout\(showToast, Math\.floor\(Math\.random\(\) \* 10000\) \+ 5000\);
  \}'''

js_replacement = r'''  let names = ["Maria C. (SP)", "Sônia R. (RJ)", "Lúcia T. (MG)", "Aparecida M. (RS)", "Helena S. (PR)", "Fátima V. (SC)", "Neuza B. (GO)", "Tereza G. (BA)", "Ivone M. (PE)", "Elza S. (CE)"];
  if(socialToast) {
    // Shuffle names array
    for(let i = names.length - 1; i > 0; i--){
      const j = Math.floor(Math.random() * (i + 1));
      [names[i], names[j]] = [names[j], names[i]];
    }

    function showToast() {
      if(names.length === 0) return; // Stop when out of names
      
      const currentName = names.pop();
      stName.innerHTML = <strong></strong>;
      socialToast.classList.add('show');
      if (navigator.vibrate) { try{ navigator.vibrate([30, 50, 30]); } catch(e){} }
      setTimeout(() => { 
        socialToast.classList.remove('show'); 
        if(names.length > 0) {
          setTimeout(showToast, Math.floor(Math.random() * 25000) + 12000); // 12s to 37s
        }
      }, 6000);
    }
    setTimeout(showToast, Math.floor(Math.random() * 10000) + 5000);
  }'''

html = re.sub(js_target, js_replacement, html)

with open('index_premium.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Done updating")
