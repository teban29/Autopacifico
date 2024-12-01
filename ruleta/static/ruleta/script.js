let container = document.querySelector(".container");
let btn = document.getElementById("spin");
const overlay = document.getElementById("overlay");

// Configurar probabilidades (en el mismo orden que las casillas)
let premios = [
    { nombre: "Gracias por participar", probabilidad: 20 },
    { nombre: "Bono $50,000", probabilidad: 8 },
    { nombre: "Gracias por participar", probabilidad: 20 },
    { nombre: "Bono $100,000", probabilidad: 6 },
    { nombre: "Gracias por participar", probabilidad: 20 },
    { nombre: "Bono $150,000", probabilidad: 4 },
    { nombre: "Gracias por participar", probabilidad: 20 },
    { nombre: "Bono $200,000", probabilidad: 2 },
];

// Función para seleccionar un premio basado en las probabilidades
function seleccionarPremio() {
    let total = premios.reduce((sum, premio) => sum + premio.probabilidad, 0);
    let random = Math.random() * total;

    let acumulado = 0;
    for (let i = 0; i < premios.length; i++) {
        acumulado += premios[i].probabilidad;
        if (random <= acumulado) {
            return i; // Retorna el índice del premio seleccionado
        }
    }
}

// Si ya hay un resultado, deshabilitar interacción y mostrar overlay
if (btn.disabled) {
    overlay.classList.add("mostrar");
}

btn.onclick = function () {
    let seleccionado = seleccionarPremio(); // Determina el índice del premio
    let gradosPorSegmento = 360 / premios.length; // Grados de cada segmento
    let gradosSeleccionados = gradosPorSegmento * seleccionado; // Grados donde comienza el segmento seleccionado
    let ajusteInicial = 22.5; // Compensación para alinear el primer segmento con la flecha
    let rotacionFinal = (360 * 5) + (360 - (gradosSeleccionados + ajusteInicial)); // Giros completos + ajuste

    // Rotar la ruleta
    container.style.transform = `rotate(${rotacionFinal}deg)`;

    // Bloquear el botón inmediatamente
    btn.disabled = true;

    // Mostrar el mensaje después de la animación de la ruleta
    setTimeout(() => {
        const premioGanado = premios[seleccionado].nombre;

        // Mostrar mensaje dependiendo del premio
        if (premioGanado === "Gracias por participar") {
            mostrarMensajeSinPremio("😞 Gracias por participar, ¡mejor suerte la próxima vez!");
        } else {
            mostrarMensajePremio(`🎉 ¡Felicidades! Ganaste ${premioGanado} 🎉`);
        }

        // Retrasar el efecto de difuminado hasta después de la animación
        setTimeout(() => {
            overlay.classList.add("mostrar");
        }, 10); // 1 segundo después del mensaje

        // Guardar resultado en el servidor
        fetch(resultadoUrl, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value,
            },
            body: JSON.stringify({ premio: premioGanado }),
        })
            .then(response => {
                if (response.ok) {
                    return response.json();
                } else {
                    console.error("Error al enviar el resultado al servidor.");
                }
            })
            .then(data => {
                console.log("Resultado guardado:", data);
            })
            .catch(error => console.error("Error:", error));
    }, 5000); // Tiempo de espera por la animación de la ruleta
};

// Función para mostrar mensaje de premio
function mostrarMensajePremio(mensaje) {
    const mensajePremio = document.getElementById("mensaje-premio");
    mensajePremio.textContent = mensaje;
    mensajePremio.classList.remove("oculto");
    mensajePremio.classList.add("mostrar");
}

// Función para mostrar mensaje de sin premio
function mostrarMensajeSinPremio(mensaje) {
    const mensajeSinPremio = document.getElementById("mensaje-sin-premio");
    mensajeSinPremio.textContent = mensaje;
    mensajeSinPremio.classList.remove("oculto");
    mensajeSinPremio.classList.add("mostrar");
}
