<script>

  import * as d3 from "d3"
  import { onMount } from "svelte"
  import { parse } from "papaparse";
  import obras_raw from "/src/data/Datos_Banksy.csv?raw"
  import main_obras_raw from "/src/data/main_obras.csv?raw"; // Importa el archivo como texto

  const options = {
    delimiter: ";", // Configura el delimitador como punto y coma
    header: true,   // Opcional: Indica si el CSV tiene encabezados
  };

  const processCSV = (raw) => {
    const parsedData = parse(main_obras_raw, options);
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

  let currentPage = 0; // Índice de la página actual
  const totalPages = 3; // Número total de páginas
  let isScrolling = false; // Evita desplazamientos repetidos mientras la animación está en curso

  const handleWheel = (event) => {
    let posScroll = window.scrollY + window.innerHeight;
    if (isScrolling || posScroll > totalPages*window.innerHeight) return; // No hacer nada si ya estamos desplazando o estamos fuera de las primeras paginas

    const newPage =
      event.deltaY > 0
        ? Math.min(currentPage + 1, totalPages - 1) // Avanza si hay más páginas
        : Math.max(currentPage - 1, 0); // Retrocede si no estamos en la primera

    if (newPage !== currentPage) {
      currentPage = newPage;
      console.log("Voy a ir a:", currentPage);
      scrollToPage(currentPage);
    }
  };

  const scrollToPage = (page) => {
    isScrolling = true; // Bloquear más scrolls
    /*window.removeEventListener("wheel", handleWheel);*/
    window.scrollTo({
      top: page * window.innerHeight,
      behavior: "instant",
    });
    // Liberar bloqueo después de la animación (duración típica de `smooth`)
    setTimeout(() => {
      isScrolling = false;
      /*window.addEventListener("wheel", handleWheel);*/
    }, 500);
  };

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("visible");
        }else{
          entry.target.classList.remove("visible");
        }
      });
    },
    {
      threshold: 0.1, // La sección debe estar al menos un 10% visible para activarse
    }
  );


  onMount(() => {
    console.log("Página cargada");
    loadFlourishScrolly()

    window.addEventListener("wheel", handleWheel);
    
    

    // Selecciona todas las secciones con la clase 'fade-in'
    const elements = document.querySelectorAll(".page");
    console.log(elements);
    elements.forEach((el) => observer.observe(el));

    return () => {
      elements.forEach((el) => observer.unobserve(el));
      window.removeEventListener("wheel", handleWheel);
    };

  });
</script>

<main>
  <section id="header" class="page">
    <h1 id="main_title">Finding Banksy</h1>
    <img src="/images/down_arrows.png" alt="flechas" class="flechas"/>

  </section>

  <section class="page">
    <img src="/images/snape.png" alt="snape" style="max-height:50vh"/>
    <div class="text-container">
      <p>Qué onda maestro? Soy el moderfokin Sneip y vamo a buscar a Banksy</p>
    </div>  
    <img src="/images/down_arrows.png" alt="flechas" class="flechas"/>
  </section>

  <section class="page">
    <img src="/images/snape.png" alt="snape" style="max-height:50vh"/>
    <div class="text-container">
      <p>jujuuuu</p>
    </div>  
    <img src="/images/down_arrows.png" alt="flechas" class="flechas"/>
  </section>

  <div id="my-wrapper">
    <div class="flourish-embed" data-src="story/2727202" data-url="https://flo.uri.sh/story/2727202/embed" data-height="100vh">
    
    </div>
    {#each main_obras as obra, index}
      <a class="card" href={"#story/2727202/slide-" + (index + 1)} style="width:{window.innerWidth*0.75}px">
        <h3 style="position:relative">{obra.Titulo}</h3>
        <div class="obra_info" style="height: {window.innerHeight*0.5}px">
          <div class="codificacion">
            <img src="/images/{tematicas[obra.Tematica]}" alt="{obra.Tematica}" class="tematica {obra.Estado == 'Vandalizada' ? 'vandalizada' : ''}" />
            <img src="/images/{Math.round(cant_splash(parseInt(obra.Valor)))}_{tecnicas[obra.Tecnica]}.png" alt="{obra.Tecnica}" class="tecnica" />
            {#if obra.Estado == "Removida"}
              <img src="/images/cruz.png" alt="Removida" style="position:absolute; z-index:2; width:30%"/>
            {/if}
          </div>
          <!---<p>{obra.Texto}</p>-->
          <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p>
        </div>
      </a>
      
    {/each}
  </div>

</main>

<style>
  .page {
    position: relative;
    width: 100vw;
    height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    scroll-snap-align: start; /* Para suavizar la navegación si el usuario hace scroll manual */
    opacity: 0;
    transition: opacity 1s ease;
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

  .card p {
    position: relative;
  }
  
  .codificacion {
    position: relative;
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .obra_info {
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
  }


  .tematica {
    position: absolute;
    z-index: 1;
    width: 45%;
  }

  .vandalizada {
    mask-image: repeating-linear-gradient(135deg, black 0%, black 2.5%, transparent 2.5%, transparent 5%);
    -webkit-mask-size: 20px 20px; /* Ajusta el tamaño de las líneas */
    mask-size: 100% 100%;
  }

  .tecnica {
    position: relative;
    width: 75%;
  }

  .text-container {
    position: relative;
    background-color: rgba(100, 100, 100, 0.5);
    padding: 20px;
    border-radius: 20px;
  }

  .flechas {
    position: absolute;
    bottom: 5%;
    width: 5%;
    animation: flash 1s ease infinite alternate;
  }

  @keyframes flash {
    from { opacity: 1; }	
    to { opacity: 0.1; }
  }

  
  h1, h3{
    color: #ffffff;
    font-family: 'PaintCans', sans-serif;
  }

  p {
    color: #ffffff;
    font-family: 'Nunito', sans-serif;
  }

</style>