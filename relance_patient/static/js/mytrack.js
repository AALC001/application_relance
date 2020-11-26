document.addEventListener("DOMContentLoaded", function(){
    //add RDV


    const formAddRDV = document.querySelector(".form-add-rdv [type='hidden']")
    const formAddRelanceCrsToken = document.querySelector(".form-add-rdv")
    const rdvDate = document.querySelector(".form-add-rdv #date_rdv")
    const codePatient = document.querySelector(".form-add-rdv #patient_code")
    const motifRdv = document.querySelector(".form-add-rdv #motif")
    // const commentRdv = document.querySelector(".form-add-rdv #")
    if(formAddRDV){
        formAddRDV.addEventListener("submit", function(e) {
            e.preventDefault()

            let constraints={}
            let validators=[]

            constraints = {
            date : {
                    presence: {message:"est réquis", allowEmpty:false}
                },

            code_patient:{
                presence: {message:"est requis", allowEmpty:false},
                format:{
                    pattern:"[0-9]{4}[\/][0-9]{2}[\/][0-9]{5}",
                    flags:"gi",
                    message:"n'est pas correct"
                }
            },
            motif={
                presence:{message:"est requis", allowEmpty:false}
            },
            // comment={
            //     presence:{message:"est requis", allowEmpty:false}
            // }
            }

            validators = validate({
                date:rdvDate.value,
                code_patient:codePatient,
                motif:motifRdv,
                // comment:commentRdv,
            }, constraints)
        })} else{
            constraints = {
                date:{
                    presence:{message:"est requis"},
                },
                code_patient = {
                    presence:{message:"est requis"},
                    format:{
                        pattern:"[0-9]{4}[\/][a-z1-Z0-9]{2}[0-9]{2}[\/][0-9]{5}",
                        flags:"gi",
                        message:"n'est pas correct"
                    }
                },
            }
            validators = validate({
                date:rdvDate.value,
                code_patient:codePatient,
                motif:motifRdv,
                // comment:commentRdv,
            }, constraints)
        }
})