const agentsDict = window.agentsDict || {};
const CLASS_ORDER = ["duelist", "initiator", "controller", "sentinel"];
const CLASS_META = {
    duelist:    { label: "Duelist",    color: "text-danger" },
    initiator:  { label: "Initiator",  color: "text-warning" },
    controller: { label: "Controller", color: "text-success" },
    sentinel:   { label: "Sentinel",   color: "text-primary" }
};

const $slots = $("#slots-container").children();
const $palette = $("#agent-palette");
const comp = new Array(5).fill(null);

function displayName(slug) {
    return agentsDict[slug] ? agentsDict[slug].block_name : slug;
}

function agentModal() {
    return bootstrap.Modal.getOrCreateInstance("#agentModal");
}

function updateSlotUI() {
    $slots.each(function (i) {
        const agent = comp[i];
        const $slot = $(this);
        const $empty = $slot.find(".slot-empty");
        const $icon = $slot.find(".slot-icon");
        const $overlay = $slot.find(".slot-name-overlay");
        const $remove = $slot.find(".slot-remove");

        if (agent) {
            $empty.addClass("d-none");
            $icon.removeClass("d-none").attr("src", "/static/icons/" + agent + "_icon.png").attr("alt", displayName(agent));
            $overlay.removeClass("d-none").text(displayName(agent));
            $remove.removeClass("d-none");
            $slot.addClass("filled");
        } else {
            $empty.removeClass("d-none");
            $icon.addClass("d-none");
            $overlay.addClass("d-none");
            $remove.addClass("d-none");
            $slot.removeClass("filled");
        }
    });
}

function firstEmptySlot() {
    return comp.indexOf(null);
}

function addAgent(agent) {
    if (!agent) return;
    if (comp.includes(agent)) {
        showToast(displayName(agent) + " is already in your comp.");
        return;
    }
    const idx = firstEmptySlot();
    if (idx === -1) {
        showToast("Comp is full (5 agents). Clear a slot first.");
        return;
    }
    comp[idx] = agent;
    updateSlotUI();
    agentModal().hide();
}

function removeAgent(idx) {
    comp[idx] = null;
    updateSlotUI();
}

CLASS_ORDER.forEach(function (cls) {
    const meta = CLASS_META[cls];
    $palette.append($("<div>", {
        class: "class-header " + meta.color,
        text: meta.label
    }));

    Object.keys(agentsDict)
        .filter(function (slug) { return agentsDict[slug].class === cls; })
        .sort(function (a, b) { return displayName(a).localeCompare(displayName(b)); })
        .forEach(function (slug) {
            const blockName = displayName(slug);

            const $card = $("<div>", {
                class: "palette-card d-flex flex-column align-items-center gap-1 border border-white/20 bg-white/5 rounded-3 p-2 cursor-pointer",
                "data-agent": slug
            });

            const $img = $("<img>", {
                src: "/static/icons/" + slug + "_icon.png",
                alt: blockName,
                draggable: false
            });

            const $name = $("<div>", {
                class: "text-white fw-bold small text-center",
                text: blockName
            });

            $card.append($img, $name);
            $palette.append($card);

            $card.on("click", function () {
                addAgent(slug);
            });
        });
});

$("#clear-comp-btn").on("click", function () {
    comp.fill(null);
    updateSlotUI();
    showToast("Comp cleared.");
});

$slots.each(function (i) {
    const $slot = $(this);

    $slot.on("click", function (e) {
        if ($(e.target).closest(".slot-remove").length) return;
        if (comp[i]) {
            removeAgent(i);
        } else {
            agentModal().show();
        }
    });

    $slot.find(".slot-remove").on("click", function (e) {
        e.stopPropagation();
        removeAgent(i);
    });
});

$("#mapFilterMenu .dropdown-item").on("click", function (e) {
    e.preventDefault();
    $("#mapFilterMenu .dropdown-item").removeClass("active");
    $(this).addClass("active");
    $("#mapFilterBtn").text($(this).data("map"));
});

function showToast(msg) {
    $(".toast-body").text(msg);
    const bsToast = new bootstrap.Toast("#toast", { delay: 2500 });
    bsToast.show();
}

updateSlotUI();
