// Credit: Ayu Itz(https://github.com/iayushanand)
// Description: Typing effect for the home page

const text1 = "Welcome to";
const text2 = " Zencipher"
const speed = 50;


function typewriterEffect(text, elementid) {
    let i = 0;
    const typewriter = setInterval(function() {
      document.getElementById(elementid).textContent += text.charAt(i);
      i++;
      if (i > text.length) {
        clearInterval(typewriter);
      }
    }, speed);
  }
setTimeout(typewriterEffect(text1, "typerwriter-text1"), 0)

setTimeout(typewriterEffect(text2, "typerwriter-text2"), 0)



const cursor = document.getElementById("typewriter-loop")

const texts = ["Easy to use", "Double-layer secure encryption", "Open-sourced", "Free to use"]

const timeout = ms => new Promise(r => setTimeout(r, ms));


(async () => {
     await timeout(1000)
     document.getElementById("features").className = ""
     while (true) {
          for (const text of texts) {
               for (const chr of text) {
                    await timeout(50);
                    cursor.textContent += chr;
               }
               await timeout(1000);

               let i = 0;
               for (const _chr of text) {
                    await timeout(25);
                    cursor.textContent = cursor.textContent.substring(0, text.length - ++i);
               }
          }
     }
})();