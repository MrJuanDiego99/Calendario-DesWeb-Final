console.log("Hola mundo");

function seleccionar(elem){
    console.log(elem);
    var dia = elem.dataset.dia;
    var mesnom = elem.dataset.mesnom;
    var mes = elem.dataset.mes;
    var anio = elem.dataset.anio;

    console.log(dia, mesnom, mes, anio);

    $("#dia").val(dia);
    $("#mesnom").val(mesnom);
    $("#mes").val(mes);
    $("#anio").val(anio);
}


function graficar(cumplidos, noCumplidos){
    console.log(cumplidos, noCumplidos);
}
