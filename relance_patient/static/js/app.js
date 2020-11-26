
// var
const humberger = document.querySelector('.app-header__humberger')
const sidebar = document.querySelector('.app-sidebar')
const actionMenus = document.querySelectorAll('.action-menu')
const actionNavMenus = document.querySelectorAll(".action-nav-menu")
const loader = document.querySelector('.loader')
const setUserActive = document.querySelector("[data-set-status-active]")
const setUserInactive = document.querySelector("[data-set-status-inactive]")
const formSetUserActiveInactive = document.querySelector(".form-set-active-or-inactive")

// form create user
const formCreateUser = document.querySelector(".form-create-user")
const cuEmail = document.querySelector('.form-create-user #email')
const cuPassword1 = document.querySelector('.form-create-user #password1')
const cuPassword2 = document.querySelector('.form-create-user #password2')
const cuFirstName = document.querySelector('.form-create-user #first_name')
const cuLastName = document.querySelector('.form-create-user #last_name')
const cuContact = document.querySelector('.form-create-user #contact')
const crsfToken = document.querySelector(".form-create-user [type='hidden']")

const deleteUser = document.querySelectorAll(".action-nav-menu .delete-user")
const editUser = document.querySelector(".action-nav-menu .edit-user")
const showUser = document.querySelectorAll(".action-nav-menu .show-user")
const showUserModal = document.querySelector("#modal-show-user")
const closeModal = document.querySelector(".modal-close")


// Show modal content
const userShowModalEmail = document.querySelector("#modal-show-user [data-user-email]")
const userShowModalFirstName= document.querySelector("#modal-show-user [data-user-firstName]")
const userShowModalLastName = document.querySelector("#modal-show-user [data-user-lastName]")
const userShowModalContact = document.querySelector("#modal-show-user [data-user-contact]")


// Connection system
const formLogin = document.querySelector(".form-login")
const userLoginEmail = document.querySelector(".form-login #auth-email")
const userLoginPassword = document.querySelector(".form-login #auth-password")
const loginCRSFToken = document.querySelector(".form-login [type='hidden']")
const loginError = document.querySelector(".login-error")

// Listing variables *****************************
const formUploadPatientListing = document.querySelector(".form-upload-patient-file")
const patientFile = document.querySelector(".form-upload-patient-file #patient_file")
const patientFileError = document.querySelector(".form-upload-patient-file .patient_file-error")
const formPatientFileToken = document.querySelector(".form-upload-patient-file [type='hidden']")
const urlExtractPatientFile = document.querySelector(".form-upload-patient-file [name='url_extract_patient_file']")


// utilisties ************************************

function redirect(path) {
    window.location = path
}

function getExtention(str) {
    const strArr = str.split('/')
    return strArr[strArr.length - 1]
}

function fromByteToMegabyte(value) {
    return value * Math.pow(10, -6)
}

function getFileInfo(fileObj) {
    if(!fileObj) return undefined

    return {
        fileName: fileObj.name,
        fileExtension: getExtention(fileObj.type),
        fileSize: fromByteToMegabyte(fileObj.size)
    }
}


function setError(inputTarget, targetError, msg='', errorclass=''){
    errorclass.split(/ /).forEach(cls => inputTarget.classList.add(cls))
    targetError.textContent = msg
    targetError.style.display = 'block'
}

document.addEventListener("DOMContentLoaded", function(){
    // Listing var
    const btnCustomnListing = document.querySelector("[data-listing-custom]")
    const btnPredefineListing = document.querySelector("[data-listing-predefine]")
    const modalCustomListing = document.querySelector("#modal-custom-listing")


    const constraints = {
        email: {
            presence: {message: "est requis"},
            email: {
                message: "Veuillez entrer un email valide",
            },
        },

        nom: {
            presence: {message: "est requis"},
            length: {
                minimum: 2,
                message: "doit être au moins de 2 caractères"
            }
        },

        prenoms: {
            presence: {message: "est requis"},
            length: {
                minimum: 2,
                message: "doit être au moins de 2 caractères"
            }
        },

        contact: {
            presence: {message: "est requis"},
            length: {
                minimum: 8,
                message: "doit être au moins de 8 caractères"
            }
        },

        // motDePasse: {
        //     presence: {message: "est requis"},
        //     length: {
        //       minimum: 8,
        //       message: "doit être au moins de 8 caractères"
        //     },
        //     format: {
        //         pattern: /(?=(.*[0-9]))(?=.*[\!@#$%^&*()\\[\]{}\-_+=~`|:;"'<>,./?])(?=.*[a-z])(?=(.*[A-Z]))(?=(.*)).{8,}/,
        //         flags: "g",
        //         message: "doit être composé de lettres en majuscules et minisucules, de chiffes et de caractère spéciaux."
        //     }
        // },

        // confirmPassword: {
        //     equality: "motDePasse"
        // },
    };

    if(formCreateUser) {
        formCreateUser.addEventListener("submit", e => {
            e.preventDefault()

            const validators = validate({
                nom: cuFirstName.value,
                prenoms: cuLastName.value,
                contact: cuContact.value,
                // motDePasse: cuPassword1.value,
                // confirmPassword: cuPassword2.value,
                email: cuEmail.value
            }, constraints)

            if(validators === undefined) {
                loader.style.display = 'flex'
                const url = formCreateUser.getAttribute("action")
                fetch(url, {
                    method: "POST",
                    body: new FormData(formCreateUser),
                    headers: {
                        "Accept": "application/json",
                        "X-CSRFToken": crsfToken.value,
                    }
                }).then(res => res.json())
                .then(data => {
                    loader.style.display = 'none'
                    if(data.type == "error") {
                        if(data.error.label === "email") cuEmail.classList.add("error")
                        Swal.fire({
                            type: "error",
                            title: data.error.title,
                            text: data.error.message
                        })
                    }else if(data.type == "success") {
                        Swal.fire({
                            title: 'Création réussie',
                            text: data.message,
                            type: 'success',
                          }).then((result) => {
                            if (result.value) {
                              window.location.href = data.redirectLink.link
                            }
                          })   
                    }
                })
  
            } else {

                for (const error in validators) {
                   if(error === "email") {
                        cuEmail.classList.add("error")
                        cuEmail.nextElementSibling.textContent = validators[error][0]
                   }

                   if(error === "nom") {
                       cuFirstName.classList.add("error")
                       cuFirstName.nextElementSibling.textContent = validators[error][0]
                   }

                   if(error === "prenoms") {
                        cuLastName.classList.add("error")
                        cuLastName.nextElementSibling.textContent = validators[error][0]
                   }

                   if(error === "contact") {
                        cuContact.classList.add("error")
                        cuContact.nextElementSibling.textContent = validators[error][0]
                   }

                //    if(error === "motDePasse") {
                //         cuPassword1.classList.add("error")
                //         cuPassword1.nextElementSibling.textContent = validators[error][0]
                //    }

                //    if(error === "confirmPassword") {
                //         cuPassword2.classList.add("error")
                //         cuPassword2.nextElementSibling.textContent = validators[error][0]
                //    }

                }  
            }
            
        })
    }

    if(sidebar){
        if(!sidebar.classList.contains('is-show')) sidebar.classList.remove('is-show')
    }

    if(humberger) {
        humberger.addEventListener('click', function() {
            sidebar.classList.toggle('is-show')
        })
    }
    


    if(actionMenus) {
        actionMenus.forEach( menu => {
            menu.addEventListener('click', function(e) {
                const nav = this.nextElementSibling
                actionNavMenus.forEach(navMenu => (nav != navMenu) ? navMenu.classList.remove("is-show") : "")
                nav.classList.toggle("is-show")
            })
        })
    }

    
    // Set user account active 
    if(setUserActive) {
        setUserActive.addEventListener("click", function(e) {
            e.preventDefault()
            e.stopPropagation()
            const url = e.target.href

            Swal.fire({
                title: 'Activation',
                text: "Voulez-vous activer le compte de l'utilisateur ?",
                icon: 'question',
                showCancelButton: true,
                confirmButtonColor: '#465f75',
                cancelButtonColor: '#DD3738',
                confirmButtonText: 'Oui, activer',
                cancelButtonText: "Annuler"
              }).then((result) => {
                if (result.value) {
                    fetch(url , {
                        method:"POST",
                        body: new FormData(formSetUserActiveInactive),
                        headers: {
                            "Accept": "application/json",
                            "X-CSRFToken": document.querySelector('.form-set-active-or-inactive input:first-of-type').value,
                        }
                    }).then(res => res.json())
                    .then(data => {
                        Swal.fire(
                            'Activation de compte',
                            data.message,
                            'success'
                          ).then(result => {
                              if(result.value) window.location.reload()
                          })
                    })
                    .catch(err => {
                        Swal.fire(
                            'Erreur d\'activation!',
                            'Une erreur est survenue lors de l\'activation du compte, veuillez réessayer',
                            'error'
                          )
                    })
                  
                }
              })
        })
    }

    // Set user account inactive
    if(setUserInactive) {

        setUserInactive.addEventListener("click", function(e) {
            e.preventDefault()
            const url = e.target.href

            Swal.fire({
                title: 'Désactivation',
                text: "Voulez-vous désactiver le compte de l'utilisateur ?",
                icon: 'question',
                showCancelButton: true,
                confirmButtonColor: '#465f75',
                cancelButtonColor: '#DD3738',
                confirmButtonText: 'Oui, désactiver',
                cancelButtonText: "Annuler"
              }).then((result) => {
                if (result.value) {
                    fetch(url , {
                        method:"POST",
                        body: new FormData(formSetUserActiveInactive),
                        headers: {
                            "Accept": "application/json",
                            "X-CSRFToken": document.querySelector('.form-set-active-or-inactive input:first-of-type').value,
                        }
                    }).then(res => res.json())
                    .then(data => {
                        Swal.fire(
                            'Désactivation de compte',
                            data.message,
                            'success'
                          ).then(result => {
                              if(result.value) window.location.reload()
                          })
                    })
                    .catch(err => {
                        Swal.fire(
                            'Erreur de désactivation!',
                            'Une erreur est survenue lors de la désactivation du compte, veuillez réessayer',
                            'error'
                          )
                    })
                  
                }
              })
        })
    }

    // Show user info modal 
    if(showUser) {

        // Delete user
        deleteUser.forEach(btn => {
            btn.addEventListener("click", function(e) {
                e.preventDefault()
                const url = e.target.href
                const form = e.target.parentElement.parentElement
                
                Swal.fire({
                    title: 'Suppression ?',
                    text: "Voulez-vous supprimer cet utilisateur ?",
                    icon: 'question',
                    showCancelButton: true,
                    confirmButtonColor: '#465f75',
                    cancelButtonColor: '#DD3738',
                    confirmButtonText: 'Oui, supprimer',
                    cancelButtonText: "Annuler"
                  }).then((result) => {
                    if (result.value) {
                        fetch(url , {
                            method:"POST",
                            body: new FormData(form),
                            headers: {
                                "Accept": "application/json",
                                "X-CSRFToken": e.target.parentElement.parentElement.firstElementChild.value,
                            }
                        }).then(res => res.json())
                        .then(data => {
                            Swal.fire(
                                'Suppresion utilisateur',
                                data.message,
                                'success'
                              ).then(result => {
                                  if(result.value) window.location.reload()
                              })
                        })
                        .catch(err => {
                            Swal.fire(
                                'Erreur de suppression!',
                                'Une erreur est survenue lors de la suppression, veuillez réessayer',
                                'error'
                              )
                        })
                      
                    }
                  })
            })
        })

        // Show user modal
        showUser.forEach(btn => {
            btn.addEventListener("click", function(e) {
                e.preventDefault();
                const url = e.target.href
                fetch(url, {
                    method: "GET",
                    headers: {
                        "Accept": "application/json"
                    }
                }).then(res => res.json())
                .then(data => {
                    if(data.type == "error") {
                        Swal.fire({
                            title: 'Erreur',
                            text: data.message,
                            type: 'error'
                        })
                    } else if(data.type == "success") {
                        userShowModalEmail.textContent = data.content.email
                        userShowModalFirstName.textContent = data.content.firstName
                        userShowModalLastName.textContent = data.content.lastName
                        userShowModalContact.textContent = data.content.contact

                        showUserModal.style.display = "block"
                        const parent = e.target.parentElement.parentElement
                        parent.classList.remove("is-show")
                    }
                }).catch(err => {
                    Swal.fire({
                        title: 'Erreur',
                            text: "Impossoble d'afficher les détails, veuillez réessayer",
                            type: 'error'
                    })
                })
                
            })
        })
    }

    // Close user modal
    if(closeModal){
        closeModal.addEventListener("click", function(e) {
            e.preventDefault()
            showUserModal.style.display = "none"
        }) 
    }
    
    // Remove error mode on focus
    document.querySelectorAll(".form-create-user input").forEach(elment => {
        elment.addEventListener("focus", () => {
            if(elment.type != "radio") {
                elment.classList.remove('error')
                elment.nextElementSibling.textContent = ""
            }
        })
    })

    document.querySelectorAll(".form-login input").forEach(elment => {
        elment.addEventListener("focus", () => {
            if(elment.type == "text" || elment.type == "password") {
                elment.classList.remove('error')
                elment.nextElementSibling.textContent = ""
            }
        })
    })

    document.querySelectorAll(".form-profile-set-password input").forEach(elment => {
        elment.addEventListener("focus", () => {
            if(elment.type == "text" || elment.type == "password") {
                elment.classList.remove('error')
                elment.nextElementSibling.textContent = ""
            }
        })
    })

    document.querySelectorAll(".form-create-site input").forEach(elment => {
        elment.addEventListener("focus", () => {
            if(elment.type == "text" || elment.type == "password") {
                elment.classList.remove('error')
                elment.nextElementSibling.textContent = ""
            }
        })
    })

    document.querySelectorAll(".form-add-relance input").forEach(elment => {
        elment.addEventListener("focus", () => {
            if(elment.type == "text" || elment.type == "date") {
                elment.classList.remove('error')
                elment.nextElementSibling.textContent = ""
            }
        })
    })

    document.querySelectorAll(".form-add-relance select").forEach(elment => {
        elment.addEventListener("focus", () => {
            elment.classList.remove('error')
            elment.nextElementSibling.textContent = ""
        })
    })

    document.querySelectorAll(".form-edit-relance input").forEach(elment => {
        elment.addEventListener("focus", () => {
            if(elment.type == "text" || elment.type == "date") {
                elment.classList.remove('error')
                elment.nextElementSibling.textContent = ""
            }
        })
    })

    document.querySelectorAll(".form-edit-relance select").forEach(elment => {
        elment.addEventListener("focus", () => {
            elment.classList.remove('error')
            elment.nextElementSibling.textContent = ""
        })
    })

    // end remove input

    // Login ajax
    if(formLogin) {
        formLogin.addEventListener("submit", function(e) {
            e.preventDefault()

            const loginConstraints = {
                email: {
                    presence: {messsage: "est réquis"},
                    email: {
                        message: "doit être un email valide"
                    }
                },
                motDePasse: {
                    presence: {message: "est requis"},
                }           
            }

            const loginValidators = validate({
                email: userLoginEmail.value,
                motDePasse: userLoginPassword.value
            }, loginConstraints)


            if(loginValidators === undefined) {
                const url = formLogin.getAttribute("action")
                fetch(url, {
                    method:"POST",
                    body: new FormData(formLogin),
                    headers: {
                        "Accept": "application/json",
                        "X-CSRFToken": loginCRSFToken.value,
                    }
                }).then(res => res.json())
                .then(data => {
                    if(data.type == "error") {
                        loginError.textContent = data.message
                        userLoginEmail.classList.add("error")
                        userLoginPassword.classList.add("error")
                    }else if (data.type == "success") {
                        redirect(data.redirectLink)
                    }
                }).catch(err => {
                    Swal.fire({
                        title: 'Erreur de connxecion',
                        type: 'error',
                        text: 'Erreur de connexion, veuillez réessayer'
                    })
                })
            }else {
                for (const error in loginValidators) {
                    if(error === "email") {
                         userLoginEmail.classList.add("error")
                         userLoginEmail.nextElementSibling.textContent = loginValidators[error][0]
                    }
                    if(error === "motDePasse") {
                        userLoginPassword.classList.add("error")
                        userLoginPassword.nextElementSibling.textContent = loginValidators[error][0]
                   }
                }
            }
        })
    }
    // End login


    /*********************************************************************************
     ********************************  LISTING SECTION *******************************
     *********************************************************************************/

    // Custom listing
    if(btnCustomnListing) {
        btnCustomnListing.addEventListener("click", e => {
            e.preventDefault();
            modalCustomListing.style.display = "block"

        })
    }

    // upload patient list file
    if(formUploadPatientListing) {

        document.querySelectorAll(".form-upload-patient-file input").forEach(elment => {
            const excludes = ["radio", "hidden", "submit"]
            elment.addEventListener("focus", () => {
                if(!excludes.includes(elment.type)) {
                    elment.classList.remove('error')
                    elment.nextElementSibling.textContent = ""
                }
            })
        })    

        formUploadPatientListing.addEventListener("submit", e => {
            e.preventDefault();
            const defaultExt = ['xlsx', 'vnd.openxmlformats-officedocument.spreadsheetml.sheet']
            const defaultSize = 2.048
            const url = e.target.getAttribute("action")
            const formData = new FormData(formUploadPatientListing)
            const fileList = patientFile.files[0]
            const {fileExtension, fileSize} = fileList !==  undefined ? getFileInfo(fileList) : ''

            
            if(fileList === undefined) {
                setError(patientFile, patientFileError, "Veuillez charger votre fichier!", 'error')
                return false
            }
          
            if(!defaultExt.includes(fileExtension)) {
                setError(patientFile, patientFileError, "Les extentions autorisées sont: (xlsx)", 'error')
                return false
            }

            if(fileSize > defaultSize) {
                setError(patientFile, patientFileError, "La taille maximale du fichier est de 2MG", 'error')
                return false
            }

            loader.style.display = "flex"
            loader.firstElementChild.textContent = "Chargement du fichier..."
            

            fetch(url, {
                method: "POST",
                body: formData,
                headers: {
                    'X-CSRFToken': formPatientFileToken.value,
                    'Accept': 'application/json'
                }
            }).then(res => res.json())
            .then(data => {
                loader.style.display = "none"
                if(data.type == 'success') {
                    Swal.fire({
                        title: 'Enregistrment réussie',
                        text: data.message,
                        type: 'success',
                      }).then((result) => {
                        if (result.value) {
                          window.location.reload()
                        }
                    })
                }else {
                    Swal.fire({
                        type: "error",
                        title: "Erreur d'enregistrement",
                        text: data.message
                    })
                }
            })
            .catch(err => {
                loader.style.display = "none"
                Swal.fire(
                    'Fichier patient',
                    'Une erreur est survenue lors du chargement du fichier, veuillez réessayer!',
                    'error'
                )
            })

        })
    }
    // END

    // USER PROFILE
    const formProfileSetPassword = document.querySelector('.form-profile-set-password')
    const profileSetPassword1 = document.querySelector('.form-profile-set-password #password1')
    const profileSetPassword2 = document.querySelector('.form-profile-set-password #password2')
    const profileCrsfToken = document.querySelector('.form-profile-set-password [type="hidden"]')

    if(formProfileSetPassword) {
        formProfileSetPassword.addEventListener('submit', function(e){
            e.preventDefault()

            const constraints = {
                motDePasse: {
                    presence: {message: "est requis"},
                    length: {
                      minimum: 8,
                      message: "doit être au moins de 8 caractères"
                    },
                    format: {
                        pattern: /(?=(.*[0-9]))(?=.*[\!@#$%^&*()\\[\]{}\-_+=~`|:;"'<>,./?])(?=.*[a-z])(?=(.*[A-Z]))(?=(.*)).{8,}/,
                        flags: "g",
                        message: "doit être composé de lettres en majuscules et minisucules, de chiffes et de caractère spéciaux."
                    }
                },
        
                confirmPassword: {
                    equality: {
                        attribute: "motDePasse",
                        message: "n'est identique au mot de passe",
                    }
                },
            };

            const validators = validate({
                motDePasse: profileSetPassword1.value,
                confirmPassword: profileSetPassword2.value,
            }, constraints)


            if(validators == undefined) {
                loader.style.display = 'flex'
                const url = formProfileSetPassword.getAttribute("action")
                fetch(url, {
                    method: "POST",
                    body: new FormData(formProfileSetPassword),
                    headers: {
                        "Accept": "application/json",
                        "X-CSRFToken": profileCrsfToken.value,
                    }
                }).then(res => res.json())
                .then(data => {
                    loader.style.display = 'none'
                    if(data.type == "error") {
                        Swal.fire({
                            type: "error",
                            title: "Modification échouée",
                            text: data.message
                        })
                    }else if(data.type == "success") {
                        Swal.fire({
                            title: 'Modification réussie',
                            text: data.message,
                            type: 'success',
                          }).then((result) => {
                            if (result.value) {
                              window.location.reload()
                            }
                          })   
                    }
                }).catch(err => {
                    Swal.fire({
                        type: "error",
                        title: "Erreur",
                        text: "Une erreur est survenue lors du chaengement du mot de passe"
                    })
                })

            }else {
                for (const error in validators) {
                    if(error === "motDePasse") {
                         profileSetPassword1.classList.add("error")
                         profileSetPassword1.nextElementSibling.textContent = validators[error][0]
                    }
 
                    if(error === "confirmPassword") {
                        profileSetPassword2.classList.add("error")
                        profileSetPassword2.nextElementSibling.textContent = validators[error][0]
                    }
 
                 }
            }

        })
    }


    // profile info general
    const formProfileSetInfo = document.querySelector(".form-profile-set-info")
    const formProfileSetInfoEmail = document.querySelector(".form-profile-set-info #email")
    const formProfileSetInfoFirstName = document.querySelector(".form-profile-set-info #first_name")
    const formProfileSetInfoLastName = document.querySelector(".form-profile-set-info #last_name")
    const formProfileSetInfoContact = document.querySelector(".form-profile-set-info #contact")
    const formProfileSetInfoCrsfToken = document.querySelector(".form-profile-set-info [type='hidden']")

    if(formProfileSetInfo) {
        formProfileSetInfo.addEventListener('submit', function(e) {
            e.preventDefault()
            const constraints = {
                email: {
                    presence: {message: "est requis"},
                    email: {
                        message: "Veuillez entrer un email valide",
                    },
                },
        
                nom: {
                    presence: {message: "est requis"},
                    length: {
                        minimum: 2,
                        message: "doit être au moins de 2 caractères"
                    }
                },
        
                prenoms: {
                    presence: {message: "est requis"},
                    length: {
                        minimum: 2,
                        message: "doit être au moins de 2 caractères"
                    }
                },
        
                contact: {
                    presence: {message: "est requis"},
                    length: {
                        minimum: 8,
                        message: "doit être au moins de 8 caractères"
                    }
                },
            };

            const validators = validate({
                nom: formProfileSetInfoFirstName.value,
                prenoms: formProfileSetInfoLastName.value,
                contact: formProfileSetInfoContact.value,
                email: formProfileSetInfoEmail.value
            }, constraints)

            if(validators === undefined) {
                loader.style.display = 'flex'
                const url = formProfileSetInfo.getAttribute("action")
                fetch(url, {
                    method: "POST",
                    body: new FormData(formProfileSetInfo),
                    headers: {
                        "Accept": "application/json",
                        "X-CSRFToken": formProfileSetInfoCrsfToken.value,
                    }
                }).then(res => res.json())
                .then(data => {
                    loader.style.display = 'none'
                    if(data.type == "error") {
                        if(data.error.label === "email") formProfileSetInfoEmail.classList.add("error")
                        Swal.fire({
                            type: "error",
                            title: data.error.title,
                            text: data.error.message
                        })
                    }else if(data.type == "success") {
                        Swal.fire({
                            title: 'Mofication réussie',
                            text: data.message,
                            type: 'success',
                          }).then((result) => {
                            if (result.value) {
                              window.location.reload()
                            }
                          })   
                    }
                }).catch(err => {
                    loader.style.display = 'none'
                    Swal.fire({
                        type: "error",
                        title: "Erreur de modification",
                        text: "Une erreur esr survenue lors de la modification, veuillez réessayer!",
                    })
                })
  
            } else {

                for (const error in validators) {
                   if(error === "email") {
                        formProfileSetInfoFirstEmail.classList.add("error")
                        formProfileSetInfoFirstEmail.nextElementSibling.textContent = validators[error][0]
                   }

                   if(error === "nom") {
                       formProfileSetInfoFirstName.classList.add("error")
                       formProfileSetInfoFirstName.nextElementSibling.textContent = validators[error][0]
                   }

                   if(error === "prenoms") {
                        formProfileSetInfoFirstLastName.classList.add("error")
                        formProfileSetInfoFirstLastName.nextElementSibling.textContent = validators[error][0]
                   }

                   if(error === "contact") {
                        formProfileSetInfoFirstContact.classList.add("error")
                        formProfileSetInfoFirstContact.nextElementSibling.textContent = validators[error][0]
                   }
                }  
            }
        })
    }

    // END


    // SITE INFO
    const formSiteInfo = document.querySelector(".form-create-site")
    const formSiteInfoCode = document.querySelector('.form-create-site #site_code')
    const formSiteInfoName = document.querySelector('.form-create-site #site_name')
    const formSiteInfoService = document.querySelector('.form-create-site #service')
    const formSiteInfoDistrict = document.querySelector('.form-create-site #district')
    const formSiteInfoRegion = document.querySelector('.form-create-site #region')
    const formSiteInfoDirectionRegionale = document.querySelector('.form-create-site #direction_sanitaire')

    const formEditSite = document.querySelector('.form-edit-site')
    const formEditSiteCode = document.querySelector('.form-edit-site #site_code')
    const formEditSiteName = document.querySelector('.form-edit-site #site_name')
    const formEditSiteService = document.querySelector('.form-edit-site #service')
    const formEditSiteDistrict = document.querySelector('.form-edit-site #district')
    const formEditSiteRegion = document.querySelector('.form-edit-site #region')
    const formEditSiteDirectionRegionale = document.querySelector('.form-edit-site #direction_sanitaire')
    
    const formSiteInfoCrsfToken = document.querySelector('.form-create-site [type="hidden"]')
    const formEditSiteCrsfToken = document.querySelector('.form-edit-site [type="hidden"]')
    
/** Add site **/
if(formSiteInfo) {
    formSiteInfo.addEventListener('submit', function(e) {
        e.preventDefault();

        const constraints = {
            code: {
                presence: {message: "est requis", allowEmpty: false},
                length: {
                    minimum: 2,
                    message: "doit être au moins de 2 caractères"
                }
            },

            nom: {
                presence: {message: "est requis", allowEmpty: false},
                length: {
                    minimum: 2,
                    message: "doit être au moins de 2 caractères"
                }
            },

            region: {
                presence: {message: "est requis", allowEmpty: false},
                length: {
                    minimum: 2,
                    message: "doit être au moins de 2 caractères"
                }
            },

            service: {
                presence: {message: "est requis", allowEmpty: false},
                length: {
                    minimum: 2,
                    message: "doit être au moins de 2 caractères"
                }
            },

            district: {
                presence: {message: "est requis", allowEmpty: false},
                length: {
                    minimum: 2,
                    message: "doit être au moins de 2 caractères"
                }
            },

            directionRegionale: {
                presence: {message: "est requis", allowEmpty: false},
                length: {
                    minimum: 2,
                    message: "doit être au moins de 2 caractères"
                }
            },
        }

        const validators = validate({
            code: formSiteInfoCode.value,
            nom: formSiteInfoName.value,
            service: formSiteInfoService.value,
            region: formSiteInfoRegion.value,
            district: formSiteInfoDistrict.value,
            directionRegionale: formSiteInfoDirectionRegionale.value,
        }, constraints)

        if(validators === undefined) {
            loader.style.display = 'flex'
            const url = formSiteInfo.getAttribute("action")

            fetch(url, {
                method: "POST",
                body: new FormData(formSiteInfo),
                headers: {
                    "Accept": "application/json",
                    "X-CSRFToken": formSiteInfoCrsfToken.value,
                }
            }).then(res => res.json())
            .then(data => {
                loader.style.display = 'none'
                if(data.type == "error") {
                    Swal.fire({
                        type: "error",
                        title: "Création échouée",
                        text: data.error.message
                    })
                }else if(data.type == "success") {
                    Swal.fire({
                        title: 'Création réussie',
                        text: data.message,
                        type: 'success',
                      }).then((result) => {
                        if (result.value) {
                          window.location.href = data.redirectLink.link
                        }
                      })   
                }
            }).catch(err => {
                loader.style.display = 'none'
                Swal.fire({
                    type: "error",
                    title: "Erreur",
                    text: "Une erreur est survenue, veuillez réessayer!"
                })
            })

        } else {

            for (const error in validators) {
               if(error === "code") {
                    formSiteInfoCode.classList.add("error")
                    formSiteInfoCode.nextElementSibling.textContent = validators[error][0]
               }
               if(error === "nom") {
                    formSiteInfoName.classList.add("error")
                    formSiteInfoName.nextElementSibling.textContent = validators[error][0]
               }
               if(error === "region") {
                    formSiteInfoRegion.classList.add("error")
                    formSiteInfoRegion.nextElementSibling.textContent = validators[error][0]
               }
               if(error === "service") {
                    formSiteInfoService.classList.add("error")
                    formSiteInfoService.nextElementSibling.textContent = validators[error][0]
               }
               if(error === "district") {
                formSiteInfoDistrict.classList.add("error")
                formSiteInfoDistrict.nextElementSibling.textContent = validators[error][0]
                }
               if(error === "directionRegionale") {
                formSiteInfoDirectionRegionale.classList.add("error")
                formSiteInfoDirectionRegionale.nextElementSibling.textContent = validators[error][0]
                }
            }  
        } 
    })

}

//** Edit site **/
    if(formEditSite) {
        formEditSite.addEventListener('submit', function(e) {
            e.preventDefault();

            const constraints = {
                code: {
                    presence: {message: "est requis", allowEmpty: false},
                    length: {
                        minimum: 2,
                        message: "doit être au moins de 2 caractères"
                    }
                },
    
                nom: {
                    presence: {message: "est requis", allowEmpty: false},
                    length: {
                        minimum: 2,
                        message: "doit être au moins de 2 caractères"
                    }
                },
    
                region: {
                    presence: {message: "est requis", allowEmpty: false},
                    length: {
                        minimum: 2,
                        message: "doit être au moins de 2 caractères"
                    }
                },
    
                service: {
                    presence: {message: "est requis", allowEmpty: false},
                    length: {
                        minimum: 2,
                        message: "doit être au moins de 2 caractères"
                    }
                },
    
                district: {
                    presence: {message: "est requis", allowEmpty: false},
                    length: {
                        minimum: 2,
                        message: "doit être au moins de 2 caractères"
                    }
                },
    
                directionRegionale: {
                    presence: {message: "est requis", allowEmpty: false},
                    length: {
                        minimum: 2,
                        message: "doit être au moins de 2 caractères"
                    }
                },
            }
    
            const validators = validate({
                code: formEditSiteCode.value,
                nom: formEditSiteName.value,
                service: formEditSiteService.value,
                region: formEditSiteRegion.value,
                district: formEditSiteDistrict.value,
                directionRegionale: formEditSiteDirectionRegionale.value,
            }, constraints)

            if(validators === undefined) {
                loader.style.display = 'flex'
                const url = formEditSite.getAttribute("action")
    
                fetch(url, {
                    method: "POST",
                    body: new FormData(formEditSite),
                    headers: {
                        "Accept": "application/json",
                        "X-CSRFToken": formEditSiteCrsfToken.value,
                    }
                }).then(res => res.json())
                .then(data => {
                    loader.style.display = 'none'
                    if(data.type == "error") {
                        Swal.fire({
                            type: "error",
                            title: "Modification échouée",
                            text: data.error.message
                        })
                    }else if(data.type == "success") {
                        Swal.fire({
                            title: 'Modification réussie',
                            text: data.message,
                            type: 'success',
                          }).then((result) => {
                            if (result.value) {
                              window.location.href = data.redirectLink.link
                            }
                          })   
                    }
                }).catch(err => {
                    loader.style.display = 'none'
                    Swal.fire({
                        type: "error",
                        title: "Erreur",
                        text: "Une erreur est survenue, veuillez réessayer!"
                    })
                })
    
            } else {
    
                for (const error in validators) {
                    for (const error in validators) {
                        if(error === "code") {
                             formEditSiteCode.classList.add("error")
                             formEditSiteCode.nextElementSibling.textContent = validators[error][0]
                        }
                        if(error === "nom") {
                             formEditSiteName.classList.add("error")
                             formEditSiteName.nextElementSibling.textContent = validators[error][0]
                        }
                        if(error === "region") {
                             formEditSiteRegion.classList.add("error")
                             formEditSiteRegion.nextElementSibling.textContent = validators[error][0]
                        }
                        if(error === "service") {
                             formEditSiteService.classList.add("error")
                             formEditSiteService.nextElementSibling.textContent = validators[error][0]
                        }
                        if(error === "district") {
                         formEditSiteDistrict.classList.add("error")
                         formEditSiteDistrict.nextElementSibling.textContent = validators[error][0]
                         }
                        if(error === "directionRegionale") {
                         formEditSiteDirectionRegionale.classList.add("error")
                         formEditSiteDirectionRegionale.nextElementSibling.textContent = validators[error][0]
                         }
                     }
                }  
            } 
        })
    }
    // END


    // ACTIVITE DE RELANCE
        const formAddRelance = document.querySelector(".form-add-relance")
        const formAddRelanceCrsfToken = document.querySelector(".form-add-relance [type='hidden']")
        const relanceDate = document.querySelector(".form-add-relance #relance_date")
        const relancePatientCode = document.querySelector(".form-add-relance #patient_code")
        const relancePatientContact = document.querySelector(".form-add-relance #patient_contact")
        const relanceReason = document.querySelector(".form-add-relance #relance_reason")
        const relanceTypeCall = document.querySelector(".form-add-relance #relance_type_call")
        const relanceTypeVisit = document.querySelector(".form-add-relance #relance_type_visit")
        const relanceCallDuration = document.querySelector(".form-add-relance [data-call-duration]")
        const callDuration = document.querySelector(".form-add-relance #call_durantion")
        const relanceFeedback = document.querySelector(".form-add-relance #relance_feedback")
        const relanceFeedbackDescription = document.querySelector(".form-add-relance [data-feedback-description]")
        const relanceFeedbackVisitDate = document.querySelector(".form-add-relance [data-feedback-visite-date]")
        const relanceMotifReasonOther = document.querySelector('.form-add-relance [data-relance-reason-other]')

        const formEditRelance = document.querySelector(".form-edit-relance")
        const formEditRelanceCrsfToken = document.querySelector(".form-edit-relance [type='hidden']")
        const editRelanceDate = document.querySelector(".form-edit-relance #relance_date")
        const editRelancePatientCode = document.querySelector(".form-edit-relance #patient_code")
        const editRelancePatientContact = document.querySelector(".form-edit-relance #patient_contact")
        const editRelanceReason = document.querySelector(".form-edit-relance #relance_reason")
        const editRelanceTypeCall = document.querySelector(".form-edit-relance #relance_type_call")
        const editRelanceTypeVisit = document.querySelector(".form-edit-relance #relance_type_visit")
        const editRelanceCallDuration = document.querySelector(".form-edit-relance [data-call-duration]")
        const editCallDuration = document.querySelector(".form-edit-relance #call_durantion")
        const editRelanceFeedback = document.querySelector(".form-edit-relance #relance_feedback")
        const editRelanceFeedbackDescription = document.querySelector(".form-edit-relance [data-feedback-description]")
        const editRelanceFeedbackVisitDate = document.querySelector(".form-edit-relance [data-feedback-visite-date]")
        const editRelanceMotifReasonOther = document.querySelector('.form-edit-relance [data-relance-reason-other]')
        
        
        if(formAddRelance) {

            // Check if relance type is call
            if (relanceTypeCall.checked) relanceCallDuration.classList.remove("hide")
            relanceTypeCall.addEventListener("change", (e) =>{
                if(e.target.checked)  relanceCallDuration.classList.remove("hide")
            })

            relanceTypeVisit.addEventListener("change", (e) =>{
                if(e.target.checked) {
                    relanceCallDuration.classList.add("hide")
                    relanceCallDuration.childNodes.forEach(child => {
                        if(child.type == "text") child.value = ""
                    })
                }
            })

            if(relanceFeedback.value === "promesse de retour")  relanceFeedbackVisitDate.classList.remove("hide")
            relanceFeedback.addEventListener("change", e => e.target.value === "promesse de retour" ? relanceFeedbackVisitDate.classList.remove("hide") : relanceFeedbackVisitDate.classList.add("hide"))

            if(relanceReason.value === "other") relanceMotifReasonOther.classList.remove('hide')
            relanceReason.addEventListener('change', e => e.target.value === 'other' ? relanceMotifReasonOther.classList.remove('hide') : relanceMotifReasonOther.classList.add('hide'))
            
            // end feedback check
            formAddRelance.addEventListener("submit", function(e) {
                e.preventDefault()

                let constraints= {}
                let validators = []

                if(relanceTypeCall.checked) {
                    constraints = {
                        date: {
                            presence: {message: "est réquis", allowEmpty: false}
                        },
    
                        code: {
                            presence: { message: "est réquis"},
                            format: {
                                pattern: "[0-9]{4}[\/][0-9]{2}[\/][0-9]{2}[\/][0-9]{5}",
                                flags: "gi",
                                message: "n'est pas correcte"
                            }
                        },
    
                        contact: {
                            presence: {message: "est réquis", allowEmpty: false}
                        },
    
                        reason: {
                            presence: {message: 'est réquis', allowEmpty: false}
                        },

                        call: {
                            presence: {message: 'est réquis', allowEmpty: false}
                        }
                    }

                    validators = validate({
                        date: relanceDate.value,
                        code: relancePatientCode.value,
                        contact: relancePatientContact.value,
                        reason: relanceReason.value,
                        call: callDuration.value

                    }, constraints)

                }else {
                    constraints = {
                        date: {
                            presence: {message: "est réquis", allowEmpty: false}
                        },
    
                        code: {
                            presence: { message: "est réquis"},
                            format: {
                                pattern: "[0-9]{4}[\/][a-zA-Z0-9]{2}[\/][0-9]{2}[\/][0-9]{5}",
                                flags: "gi",
                                message: "n'est pas correcte"
                            }
                        },
    
                        contact: {
                            presence: {message: "est réquis", allowEmpty: false}
                        },
    
                        reason: {
                            presence: {message: 'est réquis', allowEmpty: false}
                        },
                    }

                    validators = validate({
                        date: relanceDate.value,
                        code: relancePatientCode.value,
                        contact: relancePatientContact.value,
                        reason: relanceReason.value,
                    }, constraints )
                }

                if(validators === undefined) {
                    loader.style.display = 'flex'
                    const url = formAddRelance.getAttribute("action")
        
                    fetch(url, {
                        method: "POST",
                        body: new FormData(formAddRelance),
                        headers: {
                            "Accept": "application/json",
                            "X-CSRFToken": formAddRelanceCrsfToken.value,
                        }
                    }).then(res => res.json())
                    .then(data => {
                        loader.style.display = 'none'
                        if(data.type == "error") {
                            Swal.fire({
                                type: "error",
                                title: "Ajout de relance échoué",
                                text: data.error.message
                            })
                        }else if(data.type == "success") {
                            Swal.fire({
                                title: 'Ajout de relance réussie',
                                text: data.message,
                                type: 'success',
                              }).then((result) => {
                                if (result.value) {
                                  window.location.href = data.redirectLink.link
                                }
                              })   
                        }
                    }).catch(err => {
                        loader.style.display = 'none'
                        Swal.fire({
                            type: "error",
                            title: "Erreur",
                            text: "Une erreur est survenue, veuillez réessayer!"
                        })
                    })
                }else {
                    for (const error in validators) {
                        if(error === "date") {
                            relanceDate.classList.add("error")
                            relanceDate.nextElementSibling.textContent = validators[error][0]
                        }

                        if(error === "code") {
                            relancePatientCode.classList.add("error")
                            relancePatientCode.nextElementSibling.textContent = validators[error][0]
                        }
     
                        if(error === "contact") {
                            relancePatientContact.classList.add("error")
                            relancePatientContact.nextElementSibling.textContent = validators[error][0]
                        }
     
                        if(error === "reason") {
                            relanceReason.classList.add("error")
                            relanceReason.nextElementSibling.textContent = validators[error][0]
                        }

                        if(relanceTypeCall.checked) {
                            if(error === "call") {
                                callDuration.classList.add("error")
                                callDuration.nextElementSibling.textContent = validators[error][0]
                            }
                        }
                    }
                    return false
                }

            })
        }
   

        if(formEditRelance) {
            // Check if relance type is call
            if (editRelanceTypeCall.checked) editRelanceCallDuration.classList.remove("hide")
            editRelanceTypeCall.addEventListener("change", (e) =>{
                if(e.target.checked)  editRelanceCallDuration.classList.remove("hide")
            })

            editRelanceTypeVisit.addEventListener("change", (e) =>{
                if(e.target.checked) {
                    editRelanceCallDuration.classList.add("hide")
                    // editRelanceCallDuration.childNodes.forEach(child => {
                    //     if(child.type == "text") child.value = ""
                    // })
                }
            })

            if(editRelanceFeedback.value === "promesse de retour")  editRelanceFeedbackVisitDate.classList.remove("hide")
            editRelanceFeedback.addEventListener("change", e => e.target.value === "promesse de retour" ? editRelanceFeedbackVisitDate.classList.remove("hide") : editRelanceFeedbackVisitDate.classList.add("hide"))

            if(editRelanceReason.value === "other") editRelanceMotifReasonOther.classList.remove('hide')
            editRelanceReason.addEventListener('change', e => e.target.value === 'other' ? editRelanceMotifReasonOther.classList.remove('hide') : editRelanceMotifReasonOther.classList.add('hide'))

            formEditRelance.addEventListener("submit", function(e) {
                e.preventDefault()

                let constraints = {}
                let validators = []

                if(editCallDuration) {
                    const constraints = {
                        date: {
                            presence: {message: "est réquis", allowEmpty: false}
                        },
    
                        code: {
                            presence: { message: "est réquis"},
                            format: {
                                pattern: "[0-9]{4}[\/][a-zA-Z0-9]{2}[\/][0-9]{2}[\/][0-9]{5}",
                                flags: "gi",
                                message: "n'est pas correcte"
                            }
                        },
    
                        contact: {
                            presence: {message: "est réquis", allowEmpty: false}
                        },
    
                        reason: {
                            presence: {message: 'est réquis', allowEmpty: false}
                        },
    
                        callDuration: {
                            presence: {message: 'est réquis', allowEmpty: false}
                        }
                    } 

                    validators = validate({
                        date: editRelanceDate.value,
                        code: editRelancePatientCode.value,
                        contact: editRelancePatientContact.value,
                        reason: editRelanceReason.value,
                        callDuration: editCallDuration.value
                    }, constraints )

                }else {
                    constraints = {
                        date: {
                            presence: {message: "est réquis", allowEmpty: false}
                        },
    
                        code: {
                            presence: { message: "est réquis"},
                            format: {
                                pattern: "[0-9]{4}[\/][a-zA-Z0-9]{2}[\/][0-9]{2}[\/][0-9]{5}",
                                flags: "gi",
                                message: "n'est pas correcte"
                            }
                        },
    
                        contact: {
                            presence: {message: "est réquis", allowEmpty: false}
                        },
    
                        reason: {
                            presence: {message: 'est réquis', allowEmpty: false}
                        },
                    }

                    validators = validate({
                        date: editRelanceDate.value,
                        code: editRelancePatientCode.value,
                        contact: editRelancePatientContact.value,
                        reason: editRelanceReason.value,
                    }, constraints )

                }

                
                if(validators === undefined) {
                    loader.style.display = 'flex'
                    const url = formEditRelance.getAttribute("action")
        
                    fetch(url, {
                        method: "POST",
                        body: new FormData(formEditRelance),
                        headers: {
                            "Accept": "application/json",
                            "X-CSRFToken": formEditRelanceCrsfToken.value,
                        }
                    }).then(res => res.json())
                    .then(data => {
                        loader.style.display = 'none'
                        if(data.type == "error") {
                            Swal.fire({
                                type: "error",
                                title: "Modification de relance échouée",
                                text: data.error.message
                            })
                        }else if(data.type == "success") {
                            Swal.fire({
                                title: 'Modification de relance réussie',
                                text: data.message,
                                type: 'success',
                              }).then((result) => {
                                if (result.value) {
                                  window.location.href = data.redirectLink.link
                                }
                              })   
                        }
                    }).catch(err => {
                        loader.style.display = 'none'
                        Swal.fire({
                            type: "error",
                            title: "Erreur",
                            text: "Une erreur est survenue, veuillez réessayer!"
                        })
                    })
                }else {
                    for (const error in validators) {
                        if(error === "date") {
                            editRelanceDate.classList.add("error")
                            editRelanceDate.nextElementSibling.textContent = validators[error][0]
                        }

                        if(error === "code") {
                            editRelancePatientCode.classList.add("error")
                            editRelancePatientCode.nextElementSibling.textContent = validators[error][0]
                        }
     
                        if(error === "contact") {
                            editRelancePatientContact.classList.add("error")
                            editRelancePatientContact.nextElementSibling.textContent = validators[error][0]
                        }
     
                        if(error === "reason") {
                            editRelanceReason.classList.add("error")
                            editRelanceReason.nextElementSibling.textContent = validators[error][0]
                        }
     
                        if(editCallDuration) {
                            if(error === "callDuration") {
                                editCallDuration.classList.add("error")
                                editCallDuration.nextElementSibling.textContent = validators[error][0]
                            }
                        }
                        
                    }
                    return false
                }  
                

            })
        }


        const archiveRelance = document.querySelectorAll("[data-archive-relance]")

        archiveRelance.forEach(function(btn) {
            btn.addEventListener('click', function(e) {
                e.stopPropagation()
                e.preventDefault()

                const url = e.target.href
                const form = e.target.parentElement
                
                Swal.fire({
                    title: 'Archiver ?',
                    text: "Voulez-vous archiver cet utilisateur ?",
                    icon: 'question',
                    showCancelButton: true,
                    confirmButtonColor: '#465f75',
                    cancelButtonColor: '#DD3738',
                    confirmButtonText: 'Oui, archiver',
                    cancelButtonText: "Annuler"
                    }).then((result) => {
                    if (result.value) {
                        loader.style.display = "flex"
                        fetch(url , {
                            method:"POST",
                            body: new FormData(form),
                            headers: {
                                "Accept": "application/json",
                                "X-CSRFToken": e.target.parentElement.firstElementChild.value,
                            }
                        }).then(res => res.json())
                        .then(data => {
                            loader.style.display = "none"
                            Swal.fire(
                                'Archivage de relance',
                                data.message,
                                'success'
                                ).then(result => {
                                    if(result.value) window.location.reload()
                                })
                        })
                        .catch(err => {
                            loader.style.display = "none"
                            Swal.fire(
                                'Erreur d\árchivage!',
                                'Une erreur est survenue lors de l\árchivage, veuillez réessayer',
                                'error'
                                )
                        })
                        
                    }
                    })

            })
        })

    // END


    // Filter relance by code or cc

    const searchRelance = document.querySelector("#search-relance-by-text")
    const adminRelanceTable = document.querySelector("#admin-relance")

    const filterTable = (table, search) => {
        const adminRelanceTableBody = table.children[1]
        const adminRelanceTableBodyRow = adminRelanceTableBody.children
        const filter = search.value;
        const url = document.querySelector("[name='filter-relance-table']").value
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value


        for (i = 0; i < adminRelanceTableBodyRow.length; i++) {
            td = adminRelanceTableBodyRow[i].getElementsByTagName("td");
            const search = td[td.length - 1]
            if (search) {
              txtValue = search.textContent || search.innerText;
              if (txtValue.toUpperCase().indexOf(filter.toUpperCase()) > -1) {
                adminRelanceTableBodyRow[i].style.display = "";

                const request = new Request(url, {
                    headers: {
                        'X-CSRFToken': csrftoken,
                        "Accept": "application/json",
                        "Content-Type": 'application/json',
                    },
                    body: JSON.stringify({"owner": filter}),
                    method:'POST',
                    mode: 'same-origin'
                })
                
                fetch(request)
                .then(res => console.log(res))
                .then(data => console.log(data))
                .catch(err => console.log(err))
              } else {
                adminRelanceTableBodyRow[i].style.display = "none";
              }
            } 
        }
    }

    if(searchRelance) {
        filterTable(adminRelanceTable, searchRelance)

        searchRelance.addEventListener("input", function(e) {
            filterTable(adminRelanceTable, e.target)
            const filter = e.target.value;
        })
    }
    // END

    // CHART JS
    let ctx = document.getElementById('myChart')
    const chartUrl = '/api/relances/'

    if(ctx) {
        fetch(chartUrl)
    .then((res) => res.json())
    .then(data => {
        if(data.type === "success") {
            let myChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: data.labels,
                    datasets: [{
                        label: 'Relances par mois',
                        data: data.contents,
                        backgroundColor: 'transparent',
                        borderWidth: 2,
                        borderColor: '#465f75',
                    }]
                },
                options: {
                    scales: {
                        yAxes: [{
                            ticks: {
                                beginAtZero: true,
                                stepSize: 5,
                            }
                        }]
                    }
                }
            });
        }
    })
    .catch(err => console.log(err))
    }

    // END CHART


//    PATIENT LISTING
    const formPatientListing = document.querySelector("#form-patient-listing")
    const formPatientListingRDV = document.querySelector("#form-patient-listing #listing_rdv")
    const formPatientListingType = document.querySelector("#form-patient-listing #listing_type")
    const formPatientListingIntervalStart = document.querySelector("#form-patient-listing #listing_interval_start")
    const formPatientListingIntervalEnd = document.querySelector("#form-patient-listing #listing_interval_end")
    const formPatientListingMonth = document.querySelector("#form-patient-listing #listing_month")
    const formPatientListingYear = document.querySelector("#form-patient-listing #listing_year")

    const selectTypeListing = target => {
        if(target.value === "month") {
            formPatientListingMonth.parentElement.classList.remove("hide")
            formPatientListingYear.parentElement.classList.remove("hide")

            formPatientListingIntervalStart.parentElement.classList.add("hide")
            formPatientListingIntervalEnd.parentElement.classList.add("hide")

        }else if(target.value === "interval") {
            formPatientListingIntervalStart.parentElement.classList.remove("hide")
            formPatientListingIntervalEnd.parentElement.classList.remove("hide")

            formPatientListingMonth.parentElement.classList.add("hide")
            formPatientListingYear.parentElement.classList.add("hide")

        }else {
          formPatientListingIntervalStart.parentElement.classList.add("hide")
          formPatientListingIntervalEnd.parentElement.classList.add("hide")

          formPatientListingMonth.parentElement.classList.add("hide")
          formPatientListingYear.parentElement.classList.add("hide")
        }
    }

    

    if(formPatientListing) {
        
        selectTypeListing(formPatientListingType)

         // Remove or add more input field on listing type changed
         formPatientListingType.addEventListener("change", e =>{
            selectTypeListing(e.target)
         })

         formPatientListing.addEventListener("submit", function(e){
        e.preventDefault()

        //  check if the listing rdv type is not empty
        if(formPatientListingRDV.value === "") {
            Swal.fire({title: "",type: "error",text: "Veuillez sélectionner le type de RDV"})
            formPatientListingRDV.classList.add("error")
            return false
        }

        //  check if the listing type is not empty
         if(formPatientListingType.value === "") {
                Swal.fire({title: "",type: "error",text: "Veuillez sélectionner le type de listing"})
                formPatientListingType.classList.add("error")
                return false
         }

         let typeObj = {}
         if(formPatientListingType.value === 'month'){
             typeObj['type'] = 'month'
             typeObj['listingMonth'] = formPatientListingMonth.value
             typeObj['listingYear'] = formPatientListingYear.value
         }else{
             typeObj['type'] = 'interval'
             typeObj['listingStartDate'] = formPatientListingIntervalStart.value
             typeObj['listingEndDate'] = formPatientListingIntervalEnd.value
         }

         params = {
             rdvType:formPatientListingRDV.value,
             listingType: JSON.stringify(typeObj),
         }

         path = `${window.location.origin}${formPatientListing.getAttribute("action")}`
         url = new URL(path)
             url.search = new URLSearchParams(params).toString();

         loader.style.display = "flex"
         fetch(url)
             .then(res => res.json())
             .then(data => {
                 loader.style.display = "none"
                 if(data.type === 'success') {
                     Swal.fire({title: "Génération Listing",type: "success",text: data.msg})
                         .then(result => {
                             if(result.value) window.location.reload(true)
                         })
                 }
             })
             .catch(err => Swal.fire({title: "Erreur",type: "error",text: "Une erreur est survenue lors de la génération, veuillez réessayer"}))
    })
    }

//    END PATIENT LISTING


// MISSED LISTING

const formMissedListing = document.querySelector('.form-missed-rdv')
const formMissedListingMonth = document.querySelector('.form-missed-rdv #listing_month')
const formMissedListingBtn = document.querySelector(".form-missed-rdv #btn-missed-rdv")

if(formMissedListing) {
    if (formMissedListingMonth.value == "") formMissedListingBtn.classList.add('is-disabled')

    formMissedListingMonth.addEventListener("change", function(e) {
        if(e.target.value) {
            formMissedListingBtn.classList.remove('is-disabled')
        }else {
            formMissedListingBtn.classList.add('is-disabled')
        }
    })
}

// END MISSED LISTING

// INDEXTESTING
const formAddIndex = document.querySelector(".form-add-index")
const indexTypeContact = document.querySelector(".form-add-index #type_contact")
const indexTypeContactOther = document.querySelector('.form-add-index [data-index-type-other]')

if(formAddIndex) {

    if(indexTypeContact.value === "other") indexTypeContactOther.classList.remove('hide')
    indexTypeContact.addEventListener('change', e => e.target.value === 'other' ? indexTypeContactOther.classList.remove('hide') : indexTypeContactOther.classList.add('hide'))

}


})
