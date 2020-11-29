// document.addEventListener("DOMContentLoaded", function(){
//     //ADD RDV
//     'use strict'
//     const formAddRDV = document.querySelector(".form-add-rdv");
//     const formAddRelanceCrsToken = document.querySelector(".form-add-rdv [type='hidden']");
//     const rdvDate = document.querySelector(".form-add-rdv #date_rdv");
//     const codePatient = document.querySelector(".form-add-rdv #patient_code");
//     const motifRdv = document.querySelector(".form-add-rdv #motif");
//     // const commentRdv = document.querySelector(".form-add-rdv #")
//     if(formAddRDV){
//         formAddRDV.addEventListener("submit", function(e) {
//             e.preventDefault();

//             let constraints={};
//             let validators=[];

//             constraints = {
//             date : {
//                     presence: {message:"est réquis", allowEmpty:false}
//                 },

//             code_patient:{
//                 presence: {message:"est requis", allowEmpty:false},
//                 format:{
//                     pattern:"[0-9]{4}[\/][0-9]{2}[\/][0-9]{2}[\/][0-9]{5}",
//                     flags:"gi",
//                     message:"le code patient est pas correct"
//                 }
//             },
//             motif:{
//                 presence:{message:"est requis", allowEmpty:false}
//             },
//             // comment={
//             //     presence:{message:"est requis", allowEmpty:false}
//             // }
//             }

//             validators = validate({
//                 date:rdvDate.value,
//                 code_patient:codePatient.value,
//                 motif:motifRdv.value,
//                 // comment:commentRdv,
//             }, constraints)
//             if (validators === undefined){
//                 loader.style.display = 'flex'
//                 const url = formAddRDV.getAttribute("action")
//             }
//             else{
//                 for (const error in validators) {
//                     if(error === "date") {
//                         rdvDate.classList.add("error")
//                         rdvDate.nextElementSibling.textContent = validators[error][0]
//                     }

//                     if(error === "code_patient") {
//                         codePatient.classList.add("error")
//                         codePatient.nextElementSibling.textContent = validators[error][0]
//                     }
//                     if(error === "motif") {
//                         const motifBox = document.querySelector(".vsb-main button");
//                         oldStyle.borderColor = "red!important"; 
//                         motifRdv.nextElementSibling.textContent = validators[error][0];
//                     }
//                 }
//                 return false
//             }
//      })
//     }


//     // ADD CHARGE VIRALE

//         const formAddCV=document.querySelector(".form-add-cv")
//         const formAddCvCrsToken = document.querySelector(".form-add-cv [type='hidden']");
//         const cvDate=document.querySelector(".form-add-cv #cv_date")
//         const cvCodePatient=document.querySelector(".form-add-cv #patient_code")
//         const cvResult=document.querySelector(".form-add-cv #charge_virale")
//         const cvComment=document.querySelector(".form-add-cv #charge_comment")
//         if(formAddCV){
//             formAddCV.addEventListener("submit", function(e){
//                 e.preventDefault();

//                 let constraints
//                 let validators
//                 constraints={
//                     date:{
//                         presence:{message:" est requise!", allowEmpty:false}
//                     },
//                     code_patient:{
//                         presence:{message:" est requis !", allowEmpty:false},
//                         format:{
//                             pattern:"[0-9]{4}[\/][0-9]{2}[\/][0-9]{2}[\/][0-9]{5}",
//                             flags:"gi",
//                             message:" est pas correct !"
//                         }
//                     },
//                     resultat:{
//                         presence:{message:" est obligatoire !", allowEmpty:false}
//                     },
//                     comment:{
//                         presence:{message:"entrez un commentaire", allowEmpty:true}
//                     },
//                 }
//                 validators = validate({
//                     date:cvDate.value,
//                     code_patient:cvCodePatient.value,
//                     resultat:cvResult.value,
//                     comment:cvComment.value,
//                 }, constraints)
//                 if(validators==undefined){
//                     loader.style.display = 'flex'
//                     const url = formAddCV.getAttribute("action")
//                     fetch(url, {
//                         method: "POST",
//                         body: new FormData(formAddCV),
//                         headers: {
//                             "Accept": "application/json",
//                             "X-CSRFToken": formAddCvCrsToken.value,
//                         }
//                     }).then(res => res.json())
//                     .then(data => {
//                         loader.style.display = 'none'
//                         if(data.type == "error") {
//                             Swal.fire({
//                                 type: "error",
//                                 title: "Création échouée",
//                                 text: data.error.message
//                             })
//                         }else if(data.type == "success") {
//                             Swal.fire({
//                                 title: 'Création réussie',
//                                 text: data.message,
//                                 type: 'success',
//                               }).then((result) => {
//                                 if (result.value) {
//                                   window.location.href = data.redirectLink.link
//                                 }
//                               }).catch(err => {
//                                 loader.style.display = 'none'
//                                 Swal.fire({
//                                     type: "error",
//                                     title: "Erreur",
//                                     text: "Une erreur est survenue, veuillez réessayer!"
//                                 })
//                             })
//                         }
//                     })
//                 }
//                 else{
//                     for (const error in validators) {
//                         if(error === "date") {
//                             cvDate.classList.add("error")
//                             cvDate.nextElementSibling.textContent = validators[error][0]
//                         }
//                         if(error === "code_patient") {
//                             cvCodePatient.classList.add("error")
//                             cvCodePatient.nextElementSibling.textContent = validators[error][0]
//                         }

//                         if(error === "resultat") {
//                             cvResult.classList.add("error")
//                             cvResult.nextElementSibling.textContent = validators[error][0]
//                         }
//                         if(error === "comment") {
//                             const motifBox = document.querySelector(".vsb-main button");
//                             oldStyle.borderColor = "red!important"; 
//                             cvComment.nextElementSibling.textContent = validators[error][0];
//                         }
//                         }
//                     return false
//                     }
//                 })}
//             })