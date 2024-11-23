<script>

  import * as d3 from "d3"
  import { onMount } from "svelte"
  import { parse } from "papaparse";
  import obras_raw from "/src/data/Datos_Banksy_corregido.csv?raw"
  import main_obras_raw from "/src/data/main_obras.csv?raw"; // Importa el archivo como texto

  const options = {
    delimiter: ";", // Configura el delimitador como punto y coma
    header: true,   // Opcional: Indica si el CSV tiene encabezados
  };

  const processCSV = (raw) => {
    const parsedData = parse(main_obras_raw, options);
    console.log(parsedData.data); // Aquí tienes los datos procesados
    return parsedData.data;
  };

  const main_obras = processCSV(main_obras_raw);
  const obras = processCSV(obras_raw);
  
  const valores = [];
  for (let i = 0; i < main_obras.length; i++) {
    valores.push(parseInt(main_obras[i].Valor));
  }

  const tematicas = {
    "Violencia": "globo_ok.png",
    "Justicia social": "ramo.png",
    "Política": "monito.png",
    "Capitalismo": "rata_ok.png",
    "Medio ambiente": "flor_ok.png",
  }

  const tecnicas = {
    "Plantilla (stencil)": "orange",
    "Pintura sobre lienzo": "red",
    "Pintura mural": "yellow",
    "Instalación": "green"
  }

  let cant_splash = d3
    .scaleLinear()
    .domain([d3.min(valores), d3.max(valores)])
    .range([1, 4])


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
  <section id="header" class="page">
    <h1 id="main_title">
      Finding Banksy
    </h1>
  </section>

  <section class="page">
    <img src="/images/snape.png" alt="snape" style="max-height:50vh"/>
    <div class="text-container">
      <p>Qué onda maestro? Soy el moderfokin Sneip y vamo a buscar a Banksy</p>
    </div>  
  </section>

  <div id="my-wrapper">
    <div class="flourish-embed" data-src="story/2727202" data-url="https://flo.uri.sh/story/2727202/embed" data-height="100vh">
    
    </div>
    {#each main_obras as obra, index}
      <a class="card" href={"#story/2727202/slide-" + (index + 1)}>
        <h3 style="position:relative">{obra.Titulo}</h3>
        <div class="obra">
          <img src="/images/{tematicas[obra.Tematica]}" alt="{obra.Tematica}" class="tematica {obra.Estado == 'Vandalizada' ? 'vandalizada' : ''}" />
          <img src="/images/{Math.round(cant_splash(parseInt(obra.Valor)))}_{tecnicas[obra.Tecnica]}.png" alt="{obra.Tecnica}" class="tecnica" />
          {#if obra.Estado == "Removida"}
            <img src="/images/cruz.png" alt="Removida" style="position:absolute; z-index:2; width:30%"/>
          {/if}
        </div>
      </a>
      
    {/each}
  </div>

</main>

<style>
  
  .page {
    width: 100vw;
    height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
  }

  h1, h3{
    color: #ffffff;
    font-family: 'PaintCans', sans-serif;
  }

  #my-wrapper {
    background: none;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    max-width: 1280px;
    padding:0% !important;
    margin-bottom: 0px !important;
  }

  .flourish-embed {
    margin: auto;
    width: 90vw;
  }

  .card {
    width: 50%;
    height: 50%;
    position: relative;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    background-color: rgba(0, 0, 0, 0.5);
    margin-top: 50%;
    margin-bottom: 50%; 
    margin-left: auto;
    margin-right: auto;
    border-radius: 20px;
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

  .text-container {
    position: relative;
    background-color: rgba(100, 100, 100, 0.5);
    padding: 20px;
    border-radius: 20px;
  }

  p {
    color: #ffffff;
    font-family: 'Nunito', sans-serif;
  }

</style>