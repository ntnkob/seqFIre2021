function buildInfoIcon(inputID,infoMessage)
{
    var iconID = inputID+'Icon'
    var panelID = inputID+'Panel'
    var infoHTML = `<i class="bi bi-question-circle-fill" style="font-size: 2rem; color:#FFD700"; id="${iconID}"></i>`;
    var panelHTML = `<div class='paneltext' id="${panelID}">${infoMessage}</div>`;
    return infoHTML+'\n'+panelHTML;
}
function buildHyperlink(hyperlinkID,hyperlinkWord)
{
    var hyperlinkHTML = `<a href="#" class="text-decoration-none" id="${hyperlinkID}">${hyperlinkWord}</a>`
    return hyperlinkHTML;
}


$(document).ready(function() {
    $('#exampleModal').modal('show');
    $('#submitanyway').click(function () {
       $('#exampleModal').modal('hide'); 
       $('#submitAnyway').val('True');
    });
    /* Adding buttons and tooltips into the website */
    // All forms
    $("label[for=multiData]").append(buildInfoIcon("multiData","Message for multiple dataset analysis mode"));

    $("label[for=copypaste_sequence]").append(buildHyperlink("clearButton","Clear"));
    $("label[for=copypaste_sequence]").append(buildHyperlink("exampleSeqButton","Load Example Alignment"));

    $("label[for=file_sequence]").append(buildInfoIcon("fileUpload","Message for file uploading"));

    // Indel forms
    $("label[for=similarity_threshold]").append(buildInfoIcon("similarityThreshold","Message for indel similarity threshold"));

    $("label[for=p_matrix]").append(buildInfoIcon("pMatrix","Message for indel substitute group"));

    $("label[for=inter_indels]").append(buildInfoIcon("interIndel","Message for inter indels"));

    $("label[for=partial]").append(buildInfoIcon("partial","Message for partial"));

    // Conservation block form
    $("label[for=percent_similarity]").append(buildInfoIcon("percentSimilarity","Message for percent similarity"));

    $("label[for=p_matrix_2]").append(buildInfoIcon("pMatrix2","Message for conservation block substitute group"));

    $("label[for=percent_accept_gap]").append(buildInfoIcon("percent_accept_gap","Message for percent accept gap"));

    $("label[for=fuse]").append(buildInfoIcon("fuse","Message for minimum size of conserved block"));

    $("label[for=blocks]").append(buildInfoIcon("blocks","Message for maximum size of non-conserved block"));

    $("label[for=strick_combination]").append(buildInfoIcon("strickCombination","Message for combination of conserved profiles"));
        
    /* Creating event handling */
    $(document).on('click','#multiDataIcon',function() {
        $("#multiDataPanel").slideToggle("slow");
    });

    $(document).on('click','#clearButton', function() {
        $('#copypaste_sequence').val("");
        $('input[name=seqType]').prop("checked",false);
    });

    $(document).on('click','#exampleSeqButton', function() {
        var exampleSequence = `>sp|P69905|HBA_HUMAN Hemoglobin subunit alpha OS=Homo sapiens GN=HBA1 PE=1 SV=2
MVLSPADKTNVKAAWGKVGAHAGEYGAEALERMFLSFPTTKTYFPHFDLSHGSAQVKGHGKKVADALTNAVAHVDDMPNALSALSDLHAHKLRVDPVNFKLLSHCLLVTLAAHLPAEFTPAVHASLDKFLASVSTVLTSKYR
>sp|P01942|HBA_MOUSE Hemoglobin subunit alpha OS=Mus musculus GN=Hba PE=1 SV=2
MVLSGEDKSNIKAAWGKIGGHGAEYGAEALERMFASFPTTKTYFPHFDVSHGSAQVKGHGKKVADALASAAGHLDDLPGALSALSDLHAHKLRVDPVNFKLLSHCLLVTLASHHPADFTPAVHASLDKFLASVSTVLTSKYR
>sp|P13786|HBAZ_CAPHI Hemoglobin subunit zeta OS=Capra hircus GN=HBZ1 PE=3 SV=2
MSLTRTERTIILSLWSKISTQADVIGTETLERLFSCYPQAKTYFPHFDLHSGSAQLRAHGSKVVAAVGDAVKSIDNVTSALSKLSELHAYVLRVDPVNFKFLSHCLLVTLASHFPADFTADAHAAWDKFLSIVSGVLTEKYR`;
        $('#copypaste_sequence').val(exampleSequence);
        $('input[id=seqType-1]').prop("checked",true);
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
    //percentSimilarity pMatrix2 percent_accept_gap fuse blocks strickCombination
    $(document).on('click','#percentSimilarityIcon',function() {
        $("#percentSimilarityPanel").slideToggle("slow");
    });

    $(document).on('click','#pMatrix2Icon',function() {
        $("#pMatrix2Panel").slideToggle("slow");
    });

    $(document).on('click','#percent_accept_gapIcon',function() {
        $("#percent_accept_gapPanel").slideToggle("slow");
    });

    $(document).on('click','#fuseIcon',function() {
        $("#fusePanel").slideToggle("slow");
    });

    $(document).on('click','#blocksIcon', function() {
        $("#blocksPanel").slideToggle("slow");
    });

    $(document).on('click','#strickCombinationIcon', function() {
        $("#strickCombinationPanel").slideToggle("slow");
    });
    
});