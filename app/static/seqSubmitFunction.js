function buildInfoIcon(inputID,infoMessage)
{
    var iconID = inputID+'Icon'
    var panelID = inputID+'Panel'
    var infoHTML = `  <i class="bi bi-question-circle-fill" style="font-size: 16px; color:#FFD700"; id="${iconID}"></i>`;
    var panelHTML = `<div class='paneltext' style="padding: 6px; font-size: 16px;" id="${panelID}">${infoMessage}</div>`;
    return infoHTML+'\n'+panelHTML;
}
function buildHyperlink(hyperlinkID,hyperlinkWord)
{
    var hyperlinkHTML = `<a href="#" class="text-decoration-none" id="${hyperlinkID}" style = "font-size: 16px;">${hyperlinkWord}</a>`
    return hyperlinkHTML;
}
function replaceTemplateIndex(value, index) {
    return value.replace(ID_RE, '$1'+index);
}

$(document).ready(function() {   
    $('#submit').click(function (){
        if ($('#newWindow').prop('checked')==true)
        {
            $('#submit').attr('formtarget', '_blank')
        }
    });
    // Modal control
    $('#exampleModal').modal('show');
    $('#submitanyway').click(function () {
       $('#exampleModal').modal('hide'); 
       $('#submitAnyway').val('True');
    });
    /* Adding buttons and tooltips into the website */
    // All forms
    $("label[for=multidata]").append(buildInfoIcon("multiData","Message for multiple dataset analysis mode"));

    $("label[for=copypaste_sequence]").append(buildInfoIcon("fasta","Message for FASTA file format"));
    $("label[for=copypaste_sequence]").append('<br>'+buildHyperlink("clearButton","Clear"));
    $("label[for=copypaste_sequence]").append('<br>'+buildHyperlink("exampleSeqButton","Load Example Alignment"));

    $("label[for=file_sequence]").append(buildInfoIcon("fileUpload","Message for file uploading"));

    // Indel forms
    $("label[for=similarity_threshold]").append(buildInfoIcon("similarityThreshold","The percentage sequence similarity required for an alignment position to be included in the consensus"));
    $("label[for=similarity_threshold]").append(`  <i class="bi bi-plus-square-fill style="font-size: 16px; color:#FFD700"; id="addRange"></i>`);
    $("#addRange").after(`  <i class="bi bi-trash-fill style="font-size: 16px; color:#FFD700"; id="delRange"></i>`);
    $("label[for=similarity_threshold]").after(buildHyperlink("setParamIndelButton","Set all parameter values to default"));
    var fieldCount = $("form>fieldset").first().children().length - 1 //The first label is counted, so we have to subtract it out
    $('#addRange').click(function () {
        if (fieldCount<5) 
        {
            newForm = $("form>fieldset").first().children().last().clone()
            console.log("Changing threshold-"+(fieldCount-1).toString()+" to "+(fieldCount).toString())
            newForm.html(newForm.html().replace("Threshold-"+(fieldCount-1).toString(),"Threshold-"+(fieldCount).toString()))
            newForm.find('label, input').each(function() {
                var $item = $(this);
                if ($item.is('label')) {
                    $item.attr('for', $item.attr('for').replace("threshold-"+(fieldCount-1).toString(),"threshold-"+(fieldCount).toString()));
                    return;
                }
                $item.attr('id', $item.attr('id').replace("threshold-"+(fieldCount-1).toString(),"threshold-"+(fieldCount).toString()));
                $item.attr('name', $item.attr('name').replace("threshold-"+(fieldCount-1).toString(),"threshold-"+(fieldCount).toString()));
            });
            fieldCount = fieldCount+1
            $("form>fieldset").first().append("<fieldset>"+newForm.html()+"</fieldset>")
        }
        else {
            alert("Full row")
        }
    });

    $('#delRange').click(function () {
        if (fieldCount>1) {
            $("form>fieldset").first().children().last().remove()
            fieldCount = fieldCount-1
        }
        else {
            alert("At least one range is required")
        }
    });

    $("label[for=p_matrix]").append(buildInfoIcon("pMatrix","The amino acid substitution model for scoring sequence similarity"));

    $("label[for=inter_indels]").append(buildInfoIcon("interIndel","Minimum number of consensus sites required between two indels"));

    $("label[for=partial]").append(buildInfoIcon("partial","Searching in the terminal ends of the alignment to find incomplete sequence(s) (threshold for partial) treatment = 40%)"));

    // Conservation block form
    $("label[for=percent_similarity]").append(buildInfoIcon("percentSimilarity","The percentage sequence similarity required for an alignment position to be included in the consensus"));
    $("label[for=percent_similarity]").append(`  <i class="bi bi-plus-square-fill style="font-size: 16px; color:#FFD700"; id="addConservedRange"></i>`);
    $("#addConservedRange").after(`  <i class="bi bi-trash-fill style="font-size: 16px; color:#FFD700"; id="delConservedRange"></i>`);
    $("label[for=percent_similarity]").after(buildHyperlink("setParamConservedButton","Set all parameter values to default"));
    var conservedFieldCount = $("form>fieldset").last().children().length - 1 //The first label is counted, so we have to subtract it out
    $('#addConservedRange').click(function () {
        if (conservedFieldCount<5) 
        {
            newForm = $("form>fieldset").last().children().last().clone()
            console.log("Changing conserved threshold-"+(conservedFieldCount-1).toString()+" to "+(conservedFieldCount).toString())
            newForm.html(newForm.html().replace("Similarity-"+(conservedFieldCount-1).toString(),"Similarity-"+(conservedFieldCount).toString()))
            newForm.find('label, input').each(function() {
                var $item = $(this);
                if ($item.is('label')) {
                    $item.attr('for', $item.attr('for').replace("similarity-"+(conservedFieldCount-1).toString(),"similarity-"+(conservedFieldCount).toString()));
                    return;
                }
                $item.attr('id', $item.attr('id').replace("similarity-"+(conservedFieldCount-1).toString(),"similarity-"+(conservedFieldCount).toString()));
                $item.attr('name', $item.attr('name').replace("similarity-"+(conservedFieldCount-1).toString(),"similarity-"+(conservedFieldCount).toString()));
            });
            conservedFieldCount = conservedFieldCount+1
            $("form>fieldset").last().append("<fieldset>"+newForm.html()+"</fieldset>")
        }
        else {
            alert("Full row")
        }
    });

    $('#delConservedRange').click(function () {
        if (conservedFieldCount>1) {
            $("form>fieldset").last().children().last().remove()
            conservedFieldCount = conservedFieldCount-1
        }
        else {
            alert("At least one range is required")
        }
    });

    $("label[for=p_matrix_2]").append(buildInfoIcon("pMatrix2","The amino acid substitution model for scoring sequence similarity (DNA sequence: NONE)"));

    $("label[for=percent_accept_gap]").append(buildInfoIcon("percent_accept_gap","A cut off to tell the program what percentage of gaps (ratio of gaps per column) should be retained or discarded in gapped positions in the conserved block"));

    $("label[for=fuse]").append(buildInfoIcon("fuse","The minimum number of adjacent positions in the alignment used as a criterion to determine a conserved block"));

    $("label[for=blocks]").append(buildInfoIcon("blocks","The maximum number of poorly conserved (absent from consensus) alignment that are allowed to be part of a conserved block"));

    $("label[for=strick_combination]").append(buildInfoIcon("strickCombination","The resulting profiles, similarity and entropy, can be combined"));
        
    /* Creating event handling */
    $(document).on('click','#multiDataIcon',function() {
        $("#multiDataPanel").slideToggle("slow");
    });

    $(document).on('click','#fastaIcon',function() {
        $("#fastaPanel").slideToggle("slow");
    });

    $(document).on('click','#clearButton', function() {
        $('#copypaste_sequence').val("");
        $('input[name=seqType]').prop("checked",false);
    });

    $(document).on('click','#setParamIndelButton', function() {
        $('#similarity_threshold-0-start_range').val("75");
        $('#similarity_threshold-0-end_range').val("100");
        $('select[id=p_matrix]').val("NONE");
        $('#inter_indels').val("3");
        $('input[name=partial][value=False]').prop("checked",true);
    });

    $(document).on('click','#setParamConservedButton', function() {
        $('#percent_similarity-0-start_range').val("75");
        $('#percent_similarity-0-end_range').val("100");
        $('select[id=p_matrix_2]').val("NONE");
        $('#percent_accept_gap').val("40");
        $('#fuse').val("3");
        $('#blocks').val("3");
        $('input[name=strick_combination][value=False]').prop("checked",true);
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

    $("input[id=seqType-0]").click(function () {
        $("select[id=p_matrix]").val("NONE");
        $("select[id=p_matrix]").attr("disabled",true);
        $("select[id=p_matrix_2]").val("NONE");
        $("select[id=p_matrix_2]").attr("disabled",true);
    });

    $("input[id=seqType-1]").click(function () {
        $("select[id=p_matrix]").attr("disabled",false);
        $("select[id=p_matrix_2]").attr("disabled",false);
    });
    
});