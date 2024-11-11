(function (window, document, $, undefined) {
    "use strict";
  
    var PortdexAIJs = {
      i: function (e) {
        PortdexAIJs.d();
        PortdexAIJs.methods();
      },
  
      d: function (e) {
        (this._window = $(window)),
          (this._document = $(document)),
          (this._body = $("body")),
          (this._html = $("html"));
      },
  
      methods: function (e) {
        PortdexAIJs.smothScroll();
        PortdexAIJs.counterUpActivation();
        PortdexAIJs.wowActivation();
        PortdexAIJs.headerTopActivation();
        PortdexAIJs.headerSticky();
        PortdexAIJs.salActive();
        PortdexAIJs.popupMobileMenu();
        PortdexAIJs.popupDislikeSection();
        PortdexAIJs.popupleftdashboard();
        PortdexAIJs.popuprightdashboard();
        PortdexAIJs.preloaderInit();
        PortdexAIJs.showMoreBtn();
        PortdexAIJs.masonryActivation();
        PortdexAIJs.magnigyPopup();
        PortdexAIJs.lightBoxJs();
        PortdexAIJs.slickSliderActivation();
        PortdexAIJs.radialProgress();
        PortdexAIJs.contactForm();
        PortdexAIJs.menuCurrentLink();
        PortdexAIJs.onePageNav();
        PortdexAIJs.darkLight();
        PortdexAIJs.featherIcons();
        PortdexAIJs.selectPicker();
      },
  
      selectPicker: function () {
        $("select").selectpicker();
      },
  
      featherIcons: function () {
        feather.replace();
      },
  
      menuCurrentLink: function () {
        var current = location.pathname
  
          
        $(".dashboard-mainmenu li a").each(function () {
          var $this = $(this);
          if ($this.attr("href") === current) {
            $this.addClass("active");
            $this.parents(".has-menu-child-item").addClass("menu-item-open");
          }
        });
        $(".mainmenu li a").each(function () {
          var $this = $(this);
          if ($this.attr("href") === current) {
            $this.addClass("active");
            $this.parents(".has-menu-child-item").addClass("menu-item-open");
          }
        });
        $(".user-nav li a").each(function () {
          var $this = $(this);
          if ($this.attr("href") === current) {
            $this.addClass("active");
            $this.parents(".has-menu-child-item").addClass("menu-item-open");
          }
        });
      },
  
      smothScroll: function () {
        $(document).on("click", ".smoth-animation", function (event) {
          event.preventDefault();
          $("html, body").animate(
            {
              scrollTop: $($.attr(this, "href")).offset().top - 50,
            },
            300
          );
        });
      },
  
      lightBoxJs: function () {
        lightGallery(document.getElementById("animated-lightbox"), {
          thumbnail: true,
          animateThumb: false,
          showThumbByDefault: false,
          cssEasing: "linear",
        });
  
        lightGallery(document.getElementById("animated-lightbox2"), {
          thumbnail: true,
          animateThumb: false,
          showThumbByDefault: false,
          cssEasing: "linear",
        });
  
        lightGallery(document.getElementById("animated-lightbox3"), {
          thumbnail: true,
          animateThumb: false,
          showThumbByDefault: false,
          cssEasing: "linear",
        });
      },
  
      magnigyPopup: function () {
        $(document).on("ready", function () {
          $(".popup-video").magnificPopup({
            type: "iframe",
          });
        });
      },
  
      masonryActivation: function name(params) {
        $(window).load(function () {
          $(".masonary-wrapper-activation").imagesLoaded(function () {
            // filter items on button click
            $(".messonry-button").on("click", "button", function () {
              var filterValue = $(this).attr("data-filter");
              $(this).siblings(".is-checked").removeClass("is-checked");
              $(this).addClass("is-checked");
              $grid.isotope({
                filter: filterValue,
              });
            });
  
            // init Isotope
            var $grid = $(".mesonry-list").isotope({
              percentPosition: true,
              transitionDuration: "0.7s",
              layoutMode: "masonry",
              masonry: {
                columnWidth: ".resizer",
              },
            });
          });
        });
      },
  
      popupMobileMenu: function (e) {
        $(".hamberger-button").on("click", function (e) {
          $(".popup-mobile-menu").addClass("active");
        });
  
        $(".close-menu").on("click", function (e) {
          $(".popup-mobile-menu").removeClass("active");
          $(
            ".popup-mobile-menu .mainmenu .has-droupdown > a, .popup-mobile-menu .mainmenu .with-megamenu > a"
          )
            .siblings(".submenu, .rainbow-megamenu")
            .removeClass("active")
            .slideUp("400");
          $(
            ".popup-mobile-menu .mainmenu .has-droupdown > a, .popup-mobile-menu .mainmenu .with-megamenu > a"
          ).removeClass("open");
        });
  
        $(
          ".popup-mobile-menu .mainmenu .has-droupdown > a, .popup-mobile-menu .mainmenu .with-megamenu > a"
        ).on("click", function (e) {
          e.preventDefault();
          $(this)
            .siblings(".submenu, .rainbow-megamenu")
            .toggleClass("active")
            .slideToggle("400");
          $(this).toggleClass("open");
        });
  
        $(".popup-mobile-menu, .popup-mobile-menu .mainmenu.onepagenav li a").on(
          "click",
          function (e) {
            e.target === this &&
              $(".popup-mobile-menu").removeClass("active") &&
              $(
                ".popup-mobile-menu .mainmenu .has-droupdown > a, .popup-mobile-menu .mainmenu .with-megamenu > a"
              )
                .siblings(".submenu, .rainbow-megamenu")
                .removeClass("active")
                .slideUp("400") &&
              $(
                ".popup-mobile-menu .mainmenu .has-droupdown > a, .popup-mobile-menu .mainmenu .with-megamenu > a"
              ).removeClass("open");
          }
        );
      },
  
      popupDislikeSection: function (e) {
        $(".dislike-section-btn").on("click", function (e) {
          $(".popup-dislike-section").addClass("active");
        });
  
        $(".close-button").on("click", function (e) {
          $(".popup-dislike-section").removeClass("active");
        });
      },
  
      popupleftdashboard: function (e) {
        function updateSidebar() {
          if ($(window).width() >= 1200) {
            $(".popup-dashboardleft-btn").removeClass("collapsed");
            $(".popup-dashboardleft-section").removeClass("collapsed");
            $(".rbt-main-content").removeClass("area-left-expanded");
            $(".rbt-static-bar").removeClass("area-left-expanded");
          } else {
            $(".popup-dashboardleft-section").addClass("collapsed");
            $(".rbt-main-content").addClass("area-left-expanded");
            $(".rbt-static-bar").addClass("area-left-expanded");
          }
        }
  
        // Hide sidebars by default
        $(
          ".popup-dashboardleft-btn, .popup-dashboardleft-section, .rbt-main-content, .rbt-static-bar"
        ).hide();
  
        // Initial setup on page load
        updateSidebar();
  
        // Show sidebars after determining the appropriate state
        $(
          ".popup-dashboardleft-btn, .popup-dashboardleft-section, .rbt-main-content, .rbt-static-bar"
        ).show();
  
        // Update on window resize
        $(window).on("resize", function () {
          updateSidebar();
        });
  
        // Toggle classes on button click
        $(".popup-dashboardleft-btn").on("click", function (e) {
          $(".popup-dashboardleft-btn").toggleClass("collapsed");
          $(".popup-dashboardleft-section").toggleClass("collapsed");
          $(".rbt-main-content").toggleClass("area-left-expanded");
          $(".rbt-static-bar").toggleClass("area-left-expanded");
        });
      },
  
      popuprightdashboard: function (e) {
        function updateSidebar() {
          if ($(window).width() >= 1200) {
            $(".popup-dashboardright-btn").removeClass("collapsed");
            $(".popup-dashboardright-section").removeClass("collapsed");
            $(".rbt-main-content").removeClass("area-right-expanded");
            $(".rbt-static-bar").removeClass("area-right-expanded");
          } else {
            $(".popup-dashboardright-section").addClass("collapsed");
            $(".rbt-main-content").addClass("area-right-expanded");
            $(".rbt-static-bar").addClass("area-right-expanded");
          }
        }
        // Hide sidebars by default
        $(
          ".popup-right-btn, .popup-right-section, .rbt-main-content, .rbt-static-bar"
        ).hide();
  
        // Initial setup on page load
        updateSidebar();
  
        // Show sidebars after determining the appropriate state
        $(
          ".popup-right-btn, .popup-right-section, .rbt-main-content, .rbt-static-bar"
        ).show();
  
        // Update on window resize
        $(window).on("resize", function () {
          updateSidebar();
        });
  
        // Toggle classes on button click
        $(".popup-dashboardright-btn").on("click", function (e) {
          $(".popup-dashboardright-btn").toggleClass("collapsed");
          $(".popup-dashboardright-section").toggleClass("collapsed");
          $(".rbt-main-content").toggleClass("area-right-expanded");
          $(".rbt-static-bar").toggleClass("area-right-expanded");
        });
      },
  
      preloaderInit: function () {
        PortdexAIJs._window.on("load", function () {
          $(".preloader").fadeOut("slow", function () {
            $(this).remove();
          });
        });
      },
  
      showMoreBtn: function () {
        $.fn.hasShowMore = function () {
          return this.each(function () {
            $(this).toggleClass("active");
            $(this).text("Show Less");
            $(this).parent(".has-show-more").toggleClass("active");
            if ($(this).parent(".has-show-more").hasClass("active")) {
              $(this).text("Show Less");
            } else {
              $(this).text("Show More");
            }
          });
        };
        $(document).on("click", ".rbt-show-more-btn", function () {
          $(this).hasShowMore();
        });
      },
  
      slickSliderActivation: function () {
        $(".testimonial-activation").not(".slick-initialized").slick({
          infinite: true,
          slidesToShow: 1,
          slidesToScroll: 1,
          dots: true,
          arrows: true,
          adaptiveHeight: true,
          cssEase: "linear",
          prevArrow:
            '<button class="slide-arrow prev-arrow"><i class="feather-arrow-left"></i></button>',
          nextArrow:
            '<button class="slide-arrow next-arrow"><i class="feather-arrow-right"></i></button>',
        });
  
        $(".sm-slider-carosel-activation").not(".slick-initialized").slick({
          infinite: true,
          slidesToShow: 1,
          slidesToScroll: 1,
          dots: true,
          arrows: false,
          adaptiveHeight: true,
          cssEase: "linear",
        });
  
        $(".slider-activation").not(".slick-initialized").slick({
          infinite: true,
          slidesToShow: 1,
          slidesToScroll: 1,
          dots: true,
          arrows: true,
          adaptiveHeight: true,
          cssEase: "linear",
          prevArrow:
            '<button class="slide-arrow prev-arrow"><i class="feather-arrow-left"></i></button>',
          nextArrow:
            '<button class="slide-arrow next-arrow"><i class="feather-arrow-right"></i></button>',
        });
  
        $(".blog-carousel-activation")
          .not(".slick-initialized")
          .slick({
            infinite: true,
            slidesToShow: 3,
            slidesToScroll: 1,
            dots: true,
            arrows: false,
            adaptiveHeight: true,
            cssEase: "linear",
            responsive: [
              {
                breakpoint: 769,
                settings: {
                  slidesToShow: 2,
                  slidesToScroll: 2,
                },
              },
              {
                breakpoint: 581,
                settings: {
                  slidesToShow: 1,
                  slidesToScroll: 1,
                },
              },
            ],
          });
  
        $(".brand-carousel-activation")
          .not(".slick-initialized")
          .slick({
            infinite: true,
            slidesToShow: 6,
            slidesToScroll: 1,
            dots: true,
            arrows: true,
            adaptiveHeight: true,
            cssEase: "linear",
            prevArrow:
              '<button class="slide-arrow prev-arrow"><i class="feather-arrow-left"></i></button>',
            nextArrow:
              '<button class="slide-arrow next-arrow"><i class="feather-arrow-right"></i></button>',
            responsive: [
              {
                breakpoint: 769,
                settings: {
                  slidesToShow: 4,
                  slidesToScroll: 2,
                },
              },
              {
                breakpoint: 581,
                settings: {
                  slidesToShow: 3,
                },
              },
              {
                breakpoint: 480,
                settings: {
                  slidesToShow: 2,
                },
              },
            ],
          });
  
        $(".banner-imgview-carousel-activation")
          .not(".slick-initialized")
          .slick({
            infinite: true,
            slidesToShow: 5,
            slidesToScroll: 1,
            dots: false,
            autoplay: true,
            arrows: false,
            adaptiveHeight: true,
            centerMode: true,
            centerPadding: "100px",
            cssEase: "linear",
            prevArrow:
              '<button class="slide-arrow prev-arrow"><i class="feather-arrow-left"></i></button>',
            nextArrow:
              '<button class="slide-arrow next-arrow"><i class="feather-arrow-right"></i></button>',
            responsive: [
              {
                breakpoint: 769,
                settings: {
                  slidesToShow: 3,
                  slidesToScroll: 2,
                },
              },
              {
                breakpoint: 581,
                settings: {
                  slidesToShow: 3,
                },
              },
              {
                breakpoint: 480,
                settings: {
                  slidesToShow: 2,
                },
              },
            ],
          });
  
        $(".vedio-popup-carousel-activation")
          .not(".slick-initialized")
          .slick({
            infinite: true,
            slidesToShow: 1,
            slidesToScroll: 1,
            dots: false,
            autoplay: false,
            arrows: false,
            adaptiveHeight: true,
            centerMode: true,
            centerPadding: "200px",
            cssEase: "linear",
            prevArrow:
              '<button class="slide-arrow prev-arrow"><i class="feather-arrow-left"></i></button>',
            nextArrow:
              '<button class="slide-arrow next-arrow"><i class="feather-arrow-right"></i></button>',
            responsive: [
              {
                breakpoint: 769,
                settings: {
                  slidesToShow: 2,
                  slidesToScroll: 1,
                },
              },
              {
                breakpoint: 581,
                settings: {
                  slidesToShow: 2,
                },
              },
              {
                breakpoint: 480,
                settings: {
                  slidesToShow: 2,
                },
              },
            ],
          });
  
        $(".brand-carousel-init")
          .not(".slick-initialized")
          .slick({
            infinite: true,
            slidesToShow: 5,
            slidesToScroll: 1,
            dots: false,
            arrows: true,
            adaptiveHeight: true,
            cssEase: "linear",
            prevArrow:
              '<button class="slide-arrow prev-arrow"><i class="feather-arrow-left"></i></button>',
            nextArrow:
              '<button class="slide-arrow next-arrow"><i class="feather-arrow-right"></i></button>',
            responsive: [
              {
                breakpoint: 769,
                settings: {
                  slidesToShow: 4,
                  slidesToScroll: 2,
                },
              },
              {
                breakpoint: 581,
                settings: {
                  slidesToShow: 3,
                },
              },
              {
                breakpoint: 480,
                settings: {
                  slidesToShow: 2,
                },
              },
            ],
          });
  
        $(".about-app-activation").not(".slick-initialized").slick({
          infinite: true,
          slidesToShow: 1,
          slidesToScroll: 1,
          dots: true,
          arrows: false,
          adaptiveHeight: true,
          cssEase: "linear",
          prevArrow:
            '<button class="slide-arrow prev-arrow"><i class="feather-arrow-left"></i></button>',
          nextArrow:
            '<button class="slide-arrow next-arrow"><i class="feather-arrow-right"></i></button>',
        });
  
        $(".template-galary-activation")
          .not(".slick-initialized")
          .slick({
            infinite: true,
            slidesToShow: 3,
            slidesToScroll: 1,
            dots: true,
            arrows: true,
            adaptiveHeight: true,
            cssEase: "linear",
            centerMode: false,
            prevArrow:
              '<button class="slide-arrow prev-arrow"><i class="feather-arrow-left"></i></button>',
            nextArrow:
              '<button class="slide-arrow next-arrow"><i class="feather-arrow-right"></i></button>',
            responsive: [
              {
                breakpoint: 769,
                settings: {
                  slidesToShow: 4,
                  slidesToScroll: 2,
                },
              },
              {
                breakpoint: 581,
                settings: {
                  slidesToShow: 3,
                },
              },
              {
                breakpoint: 480,
                settings: {
                  slidesToShow: 2,
                },
              },
            ],
          });
      },
  
      salActive: function () {
        sal({
          threshold: 0.01,
          once: true,
        });
      },
  
      backToTopInit: function () {
        var scrollTop = $(".rainbow-back-top");
        $(window).scroll(function () {
          var topPos = $(this).scrollTop();
          if (topPos > 150) {
            $(scrollTop).css("opacity", "1");
          } else {
            $(scrollTop).css("opacity", "0");
          }
        });
        $(scrollTop).on("click", function () {
          $("html, body").animate(
            {
              scrollTop: 0,
              easingType: "linear",
            },
            10
          );
          return false;
        });
      },
  
      headerSticky: function () {
        $(window).scroll(function () {
          if ($(this).scrollTop() > 250) {
            $(".header-sticky").addClass("sticky");
          } else {
            $(".header-sticky").removeClass("sticky");
          }
        });
      },
  
      counterUpActivation: function () {
        $(".counter").counterUp({
          delay: 10,
          time: 1000,
        });
      },
  
      wowActivation: function () {
        new WOW().init();
      },
  
      headerTopActivation: function () {
        $(".bgsection-activation").on("click", function () {
          $(".header-top-news").addClass("deactive");
        });
      },
  
      radialProgress: function () {
        $(".radial-progress").waypoint(
          function () {
            $(".radial-progress").easyPieChart({
              lineWidth: 10,
              scaleLength: 0,
              rotate: 0,
              trackColor: false,
              lineCap: "round",
              size: 220,
            });
          },
          {
            triggerOnce: true,
            offset: "bottom-in-view",
          }
        );
      },
  
      contactForm: function () {
        $(".rainbow-dynamic-form").on("submit", function (e) {
          e.preventDefault();
          var _self = $(this);
          var __selector = _self.closest("input,textarea");
          _self.closest("div").find("input,textarea").removeAttr("style");
          _self.find(".error-msg").remove();
          _self
            .closest("div")
            .find('button[type="submit"]')
            .attr("disabled", "disabled");
          var data = $(this).serialize();
          $.ajax({
            url: "mail.php",
            type: "post",
            dataType: "json",
            data: data,
            success: function (data) {
              _self
                .closest("div")
                .find('button[type="submit"]')
                .removeAttr("disabled");
              if (data.code == false) {
                _self.closest("div").find('[name="' + data.field + '"]');
                _self
                  .find(".rainbow-btn")
                  .after('<div class="error-msg"><p>*' + data.err + "</p></div>");
              } else {
                $(".error-msg").hide();
                $(".form-group").removeClass("focused");
                _self
                  .find(".rainbow-btn")
                  .after(
                    '<div class="success-msg"><p>' + data.success + "</p></div>"
                  );
                _self.closest("div").find("input,textarea").val("");
  
                setTimeout(function () {
                  $(".success-msg").fadeOut("slow");
                }, 5000);
              }
            },
          });
        });
      },
  
      onePageNav: function () {
        $(".onepagenav").onePageNav({
          currentClass: "current",
          changeHash: false,
          scrollSpeed: 500,
          scrollThreshold: 0.2,
          filter: "",
          easing: "swing",
        });
      },
  
      darkLight: function () {
        var styleMode = document.querySelector(
          'meta[name="theme-style-mode"]'
        ).content;
        var cookieKey =
          styleMode == 1
            ? "client_dark_mode_style_cookie"
            : "client_light_mode_style_cookie";
        if (Cookies.get(cookieKey) == "dark") {
          $("body").removeClass("active-light-mode");
          $("body").addClass("active-dark-mode");
        } else if (Cookies.get(cookieKey) == "light") {
          $("body").removeClass("active-dark-mode");
          $("body").addClass("active-light-mode");
        } else {
          if (styleMode == 1) {
            $("body").addClass("active-dark-mode");
          } else {
            $("body").addClass("active-light-mode");
          }
        }
      },
    };
    PortdexAIJs.i();
  })(window, document, jQuery);
  
  // Bg flashlight
  let cards = document.querySelectorAll(".bg-flashlight");
  cards.forEach((bgflashlight) => {
    bgflashlight.onmousemove = function (e) {
      let x = e.pageX - bgflashlight.offsetLeft;
      let y = e.pageY - bgflashlight.offsetTop;
  
      bgflashlight.style.setProperty("--x", x + "px");
      bgflashlight.style.setProperty("--y", y + "px");
    };
  });
  
  // Bg flashlight
  let shapes = document.querySelectorAll(".blur-flashlight");
  shapes.forEach((bgflashlight) => {
    bgflashlight.onmousemove = function (e) {
      let x = e.pageX - bgflashlight.offsetLeft;
      let y = e.pageY - bgflashlight.offsetTop;
  
      bgflashlight.style.setProperty("--x", x + 70 + "px");
      bgflashlight.style.setProperty("--y", y + 200 + "px");
    };
  });
  
  // Tooltip
  var tooltipTriggerList = [].slice.call(
    document.querySelectorAll('[data-bs-toggle="tooltip"]')
  );
  var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
  });
  
  // Expand Textarea
  // function expandTextarea(id) {
  //     document.getElementById(id).addEventListener('keyup', function() {
  //         this.style.overflow = 'hidden';
  //         this.style.height = 0;
  //         this.style.height = this.scrollHeight + 'px';
  //     }, false);
  // }
  
  // expandTextarea('txtarea');
  
  //Check All JS Activation
  $(function () {
    var propFn = typeof $.fn.prop === "function" ? "prop" : "attr";
  
    $("#checkall").click(function () {
      $(this)
        .parents("fieldset:eq(0)")
        .find(":checkbox")
        [propFn]("checked", this.checked);
    });
    $("input[type=checkbox]:not(#checkall)").click(function () {
      if (!this.checked) {
        $("#checkall")[propFn]("checked", this.checked);
      } else {
        $("#checkall")[propFn](
          "checked",
          !$("input[type=checkbox]:not(#checkall)").filter(":not(:checked)")
            .length
        );
      }
    });
  });
  
  async function getOpenAIResponse(userMessage) {
    const response = await fetch('/api/get_openai_response/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: userMessage })
    });

    if (!response.ok) {
        console.error('Error fetching from Django:', response.statusText);
        return "Sorry, I could not get a response at this time.";
    }

    const data = await response.json();
    return data.response;  // OpenAI's response from Django
}
  
  
  async function handleFileAndMessageUpload(event, userMessage) {
    const file = event.target.files[0];
    if (!file) return;
  
    const reader = new FileReader();
  
    reader.onload = async function (e) {
      const fileContent = e.target.result;
      const queries = fileContent.split('\n').filter(query => query.trim() !== "");
  
      for (const query of queries) {
        const combinedMessage = `${userMessage}\n\n${query}`;
  
        // Display the user message and query
        const userMessageElement = createEditableMessage("You", combinedMessage, "author-speech", "assets/images/team/team-01.png");
        appendMessage(userMessageElement);
  
        // Get response from OpenAI for each combined message
        const response = await getOpenAIResponse(combinedMessage);
        const responseElement = createMessageWithReactions("PortdexAI", response, "ai-speech", "assets/images/team/avater.png");
        appendMessage(responseElement);
      }
    };
  
    reader.onerror = function () {
      console.error("Error reading file");
    };
  
    reader.readAsText(file);
  }
  
  


  async function sendMessage() {
    const txtarea = document.getElementById("txtarea");
    const fileInput = document.getElementById("fileInput");
    const chatContainer = document.getElementById("chatContainer");

    const userMessage = txtarea.value.trim();
    const files = fileInput.files;

    // Exit if there's no message and no files
    if (!userMessage && files.length === 0) return;

    // Display the user message if it exists
    let combinedMessage = userMessage;
    if (userMessage) {
        const userMessageElement = createEditableMessage(
            "You",
            userMessage,
            "author-speech",
            "assets/images/team/team-01.png"
        );
        appendMessage(userMessageElement);
    }

    // Display each file name in the chat and read the content to include in the combined message
    if (files.length > 0) {
        for (const file of files) {
            // Display the file name in chat
            const fileNameElement = createEditableMessage(
                "You",
                `📎 Attached: ${file.name}`,
                "author-speech",
                "assets/images/team/team-01.png"
            );
            appendMessage(fileNameElement);

            // Read the file content to include in the message sent to Django
            const fileContent = await readFileContent(file);
            combinedMessage += `\n\n[File: ${file.name}]\n${fileContent}`;
        }
    }
    function getCsrfToken() {
      const csrfTokenInput = document.getElementById("csrfToken");
      return csrfTokenInput ? csrfTokenInput.value : "";
  }
    const chatId =  document.getElementById("chatForm").getAttribute("data-chat-id");
    const source = document.querySelector("input[name='source']").getAttribute("value"); // Get source value

    // Send the combined message to Django with the chat_id included
    const response = await fetch(`/send_message/${chatId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCsrfToken() // Add CSRF token function if necessary
        },
        body: JSON.stringify({ userMessage: combinedMessage, source: source }) // Set source as needed
    });

    if (response.ok) {
        const data = await response.json();
        const autoReplyElement = createMessageWithReactions(
            "PortdexAI",
            data.response, // Response from Django/OpenAI
            "ai-speech",
            "assets/images/team/avater.png"
        );
        appendMessage(autoReplyElement);
    } else {
        console.error("Error sending message to Django:", response.statusText);
    }

    // Clear text area and file input after sending the message
    txtarea.value = "";
    fileInput.value = "";
}


  // Helper function to read file content as text
  function readFileContent(file) {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => resolve(reader.result);
      reader.onerror = () => reject("Error reading file");
      reader.readAsText(file);
    });
  }
  
  
  function createEditableMessage(title, message, speechClass, imgSrc) {
    const messageElement = createMessageElement(
      title,
      message,
      speechClass,
      imgSrc,
      true
    );
    return messageElement;
  }
  
  function createMessageWithReactions(title, message, speechClass, imgSrc) {
    const messageElement = createMessageElement(
      title,
      message,
      speechClass,
      imgSrc,
      false
    );
    return messageElement;
  }
  
  function createMessageElement(title, message, speechClass, imgSrc, isEditable) {
    const messageElement = document.createElement("div");
    messageElement.className = `chat-box ai-speech bg-flashlight ${speechClass}`;
    messageElement.innerHTML = `
        <div class="inner top-flashlight leftside light-xl">
          <div class="chat-section">
            
            <div class="chat-content">
              <h6 class="title">${title}</h6>
              <p class="mb--20 ${isEditable ? "editable" : ""}" ${
      isEditable ? 'contenteditable="true"' : ""
    }>${message}</p>
              ${isEditable ? getEditButtons() : getReactionButtons()}
            </div>
          </div>
        </div>
      `;
    return messageElement;
  }
  
  function getEditButtons() {
    return ' '
    // return `
    //     <div class="edit-actions">
    //       <button class="edit-btn btn-default btn-small btn-border" onclick="editMessage(this)"><i class="feather-edit"></i></button>
    //       <button class="save-regenerate-btn btn-default btn-small" onclick="saveAndRegenerateMessage(this)">Save & Regenerate</button>
    //       <button class="cancel-btn btn-default btn-small btn-border" onclick="cancelEdit(this)">Cancel</button>
    //     </div>
    //   `;
  }
  
  function getReactionButtons() {
    return `
        <div class="reaction-section">
          <div class="btn-grp">
              <div class="left-side-btn dropup">
                  
                  <button data-bs-toggle="modal" data-bs-target="#shareModal" class="react-btn btn-default btn-small btn-border"><i class="feather-share"></i></button>
                  
              </div>
              <div class="right-side-btn">
                  <button class="react-btn btn-default btn-small btn-border" onclick="copyMessage(this)">
                      <i class="feather-copy"></i><span>Copy</span>
                  </button>
              </div>
          </div>
        </div>
      `;
  }
    function copyMessage(button) {
      // Locate the message content within the same chat box element
      const messageContent = button.closest(".chat-content").querySelector("p").innerText;

      // Copy the content to the clipboard
      navigator.clipboard.writeText(messageContent)
          .then(() => {
              alert("Message copied to clipboard!");
          })
          .catch(err => {
              console.error("Failed to copy message: ", err);
          });
  }
  function appendMessage(messageElement) {
    const chatContainer = document.getElementById("chatContainer");
    const isAutoReply = messageElement.classList.contains("ai-speech");
  
    chatContainer.appendChild(messageElement);
  
    if (isAutoReply) {
      // Scroll down to reveal the auto-reply
      chatContainer.scrollTop = chatContainer.scrollHeight;
    }
  }
  
  function editMessage(button) {
    const chatContent = button.parentElement.parentElement.parentElement;
    const editable = chatContent.querySelector(".editable");
    editable.contentEditable = "true";
    editable.focus();
  }
  
  function saveAndRegenerateMessage(button) {
    const chatContent = button.parentElement.parentElement.parentElement;
    const editable = chatContent.querySelector(".editable");
    const editedMessage = editable.textContent;
    editable.contentEditable = "false";
  
    // Save the edited message (you can send it to a server, etc.)
    console.log("Saved message:", editedMessage);
  
    // Regenerate a new message
    const regeneratedMessage = generateAutoReply();
    const regeneratedMessageElement = createMessageWithReactions(
      "PortdexAI",
      regeneratedMessage,
      "ai-speech",
      "assets/images/team/avater.png"
    );
    appendMessage(regeneratedMessageElement);
  }
  
  function cancelEdit(button) {
    const chatContent = button.parentElement.parentElement.parentElement;
    const editable = chatContent.querySelector(".editable");
    editable.contentEditable = "false";
    // Optionally, you can revert the content to the original state
  }
  
  function regenerateMessage() {
    const regeneratedMessage = generateAutoReply();
    const regeneratedMessageElement = createMessageWithReactions(
      "PortdexAI",
      regeneratedMessage,
      "ai-speech",
      "assets/images/team/avater.png"
    );
    appendMessage(regeneratedMessageElement);
  }
  
  const txtarea = document.getElementById("txtarea");
  if (null !== txtarea) {
    txtarea.addEventListener("keydown", function (e) {
      if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
      }
    });
  }
  