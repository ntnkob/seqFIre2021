function buildInfoIcon(inputID,infoMessage)
{
    var iconID = inputID+'Icon'
    var panelID = inputID+'Panel'
    var infoHTML = `<i class="bi bi-question-circle-fill" style="font-size: 2rem; color:#FFD700"; id="${iconID}">`;
    var panelHTML = `<div id="${panelID}">${infoMessage}</div>`;
    return infoHTML+panelHTML;
}
function buildHyperlink(hyperlinkID,hyperlinkWord)
{
    var hyperlinkHTML = `<a href="#" class="text-decoration-none" id="${hyperlinkID}">${hyperlinkWord}</a>`
    return hyperlinkHTML;
}


$(document).ready(function() {
    /* Adding buttons and tooltips into the website */
    // All forms
    $("label[for=multiData]").append(buildInfoIcon("multiData","Message for multiple dataset analysis mode"));

    $("label[for=copypaste_sequence]").append(buildHyperlink("clearButton","Clear"));
    $("label[for=copypaste_sequence]").append(buildHyperlink("exampleSeqButton","Load Example Alignment"));

    $("label[for=file_sequence]").append(buildInfoIcon("fileUpload","Message for file uploading"));

    $("#parameterSection").append(buildHyperlink("defaultButton","Default"));

    // Indel forms
    $("label[for=similarity_threshold]").append(buildInfoIcon("similarityThreshold","Message for indel similarity threshold"));

    $("label[for=p_matrix]").append(buildInfoIcon("pMatrix","Message for indel substitute group"));

    $("label[for=inter_indels]").append(buildInfoIcon("interIndel","Message for inter indels"));

    $("label[for=partial]").append(buildInfoIcon("partial","Message for partial"));

        
    /* Creating event handling */
    $(document).on('click','#multiDataIcon',function() {
        $("#multiDataPanel").slideToggle("slow");
    });

    $(document).on('click','#clearButton', function() {
        $('#copypaste_sequence').val("");
    });

    $(document).on('click','#exampleSeqButton', function() {
        var exampleSequence = `>sp|P69905|HBA_HUMAN Hemoglobin subunit alpha OS=Homo sapiens GN=HBA1 PE=1 SV=2
MVLSPADKTNVKAAWGKVGAHAGEYGAEALERMFLSFPTTKTYFPHFDLSHGSAQVKGHG
KKVADALTNAVAHVDDMPNALSALSDLHAHKLRVDPVNFKLLSHCLLVTLAAHLPAEFTP
AVHASLDKFLASVSTVLTSKYR
>sp|P01942|HBA_MOUSE Hemoglobin subunit alpha OS=Mus musculus GN=Hba PE=1 SV=2
MVLSGEDKSNIKAAWGKIGGHGAEYGAEALERMFASFPTTKTYFPHFDVSHGSAQVKGHG
KKVADALASAAGHLDDLPGALSALSDLHAHKLRVDPVNFKLLSHCLLVTLASHHPADFTP
AVHASLDKFLASVSTVLTSKYR
>sp|P13786|HBAZ_CAPHI Hemoglobin subunit zeta OS=Capra hircus GN=HBZ1 PE=3 SV=2
MSLTRTERTIILSLWSKISTQADVIGTETLERLFSCYPQAKTYFPHFDLHSGSAQLRAHG
SKVVAAVGDAVKSIDNVTSALSKLSELHAYVLRVDPVNFKFLSHCLLVTLASHFPADFTA
DAHAAWDKFLSIVSGVLTEKYR`;
        $('#copypaste_sequence').val(exampleSequence);
    });

    $(document).on('click','#fileUploadIcon',function() {
        $("#fileUploadPanel").slideToggle("slow");
    });

    $(document).on('click','#similarityThresholdIcon',function() {
        $("#similarityThresholdPanel").slideToggle("slow");
    });

    $(document).on('click','#pMatrixIcon',function() {
        $("#pMatrixPanel").slideToggle("slow");
    });

    $(document).on('click','#interIndelIcon', function() {
        $("#interIndelPanel").slideToggle("slow");
    });

    $(document).on('click','#partialIcon',function() {
        $("#partialPanel").slideToggle("slow");
    });


    
    $("input[name=multiData]").click(function() {
        // $("input[id=multiData-0]").prop("checked", true);
        $("label[for|=multiData]").prop("disabled", true);
        $("input[name=multiData]").prop("disabled", true);
    });
    
});