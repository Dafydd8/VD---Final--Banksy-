<script>

import obras from "/src/data/Datos_Banksy_corregido.csv"
import main_obras from "/src/data/main_obras.csv"
import * as d3 from "d3"
import { onMount } from "svelte"

let obra1 = obras[0];
let valores = [];

for (let i = 0; i < obras.length; i++) {
  valores.push(parseInt(obras[i].Valor));
}

const tematicas = {
  "Violencia": "globo_ok.png",
  "Justicia social": "ramo_ok.png",
  "Política": "mono_ok.png",
  "Capitalismo": "rata_ok.png",
  "Medio ambiente": "flor_ok.png",
}

const tecnicas = {
  "Plantilla (stencil)": "orange",
  "Pintura sobre lienzo": "red",
  "Pintura mural": "yellow",
  "Instalación": "green"
}

  function loadFlourishScrolly() {
    const script = document.createElement('script')
    script.src = "https://cdn.flourish.rocks/flourish-scrolly-v3.1.0.min.js"
    script.type = "text/javascript"
    script.onload = () => initFlourishScrolly()
    document.body.appendChild(script)
  }


  onMount(() => {
    loadFlourishScrolly()
  });
</script>

<main>
  <section id="header">
    <h1 id="main_title">
      Finding Banksy
    </h1>
  </section>

  <div id="my-wrapper">
    <!-- Reemplazar el ID de ejemplo por el de la story propia -->
    <div class="flourish-embed" data-src="story/2730386" data-url="https://flo.uri.sh/story/2730386/embed" data-height="100vh">
      
      <!---<script src="https://public.flourish.studio/resources/embed.js"></script>-->
    </div>
  
    <!-- Iteramos sobre las distintas slides del componente de Flourish -->
    {#each main_obras as obra, index}
      <div class="card">
        <a href={"#story/2730386/slide-" + (index + 1)}></a>
        <div class="obra">
          <p>{obra.Titulo}</p>
          <img src="/images/{tematicas[obra.Tematica]}" alt="{obra.Tematica}" class="tematica {obra.Estado == 'Vandalizada' ? 'vandalizada' : ''}" />
          <img src="/images/1_{tecnicas[obra.Tecnica]}.png" alt="{obra.Tecnica}" class="tecnica" />
          {#if obra.Estado == "Removida"}
            <img src="/images/cruz.png" alt="Removida" style="position:absolute; z-index:2; width:30%"/>
          {/if}
        </div>
      </div>
    {/each}
  </div>

</main>

<style>
  
  #header {
    width: 100vw;
    height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
  }

  #header h1{
    color: #ffffff;
  }

  #my-wrapper {
    margin: auto;
    max-width: 1280px;

  }

  .card {
    position: relative;
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: rgba(125, 125, 125, 0.5);
    margin: 5%;
  }

  .obra {
    position: relative;
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .tematica {
    position: absolute;
    z-index: 1;
    width: 30%;
  }

  .vandalizada {
    mask-image: repeating-linear-gradient(135deg, black 0%, black 2.5%, transparent 2.5%, transparent 5%);
    -webkit-mask-size: 20px 20px; /* Ajusta el tamaño de las líneas */
    mask-size: 100% 100%;
  }

  .tecnica {
    position: relative;
    width: 50%;
  }

  a {
  font-weight: 500;
  color: #646cff;
  text-decoration: inherit;
}
  a:hover {
    color: #535bf2;
  }

</style>
