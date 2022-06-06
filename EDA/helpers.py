def group_data(data):
    output = {}
    for d in data:
        if d == 0:
            continue
        if d in output.keys():
            output[d] += 1
        else:
            output[d] = 1
    return [output]


def analyze_format(format):
    format_domain = pd.DataFrame(group_data(format["domain_collection"]))
    format_lands = pd.DataFrame(group_data(format["domain_in_Lands"]))
    format_spells = pd.DataFrame(group_data(format["domain_in_Spells"]))
    format_artifacts = pd.DataFrame(group_data(format["domain_in_Artifacts"]))
    format_enchantments = pd.DataFrame(group_data(format["domain_in_Enchantments"]))
    format_creatures = pd.DataFrame(group_data(format["domain_in_Creatures"]))
    format_planeswalkers = pd.DataFrame(group_data(format["domain_in_Planeswalkers"]))
    fig = plt.figure(figsize=(15, 15))
    ax1 = fig.add_subplot(331)
    ax2 = fig.add_subplot(332)
    ax3 = fig.add_subplot(333)
    ax4 = fig.add_subplot(334)
    ax5 = fig.add_subplot(335)
    ax6 = fig.add_subplot(336)
    # format_domain.plot(title="format",kind="bar",ax=ax1)
    format_lands.plot(title="lands", kind="bar", ax=ax2)
    format_spells.plot(title="spells", kind="bar", ax=ax3)
    format_artifacts.plot(title="artifacts", kind="bar", ax=ax4)
    format_enchantments.plot(title="enchantments", kind="bar", ax=ax5)
    format_creatures.plot(title="creatures", kind="bar", ax=ax6)
    format_planeswalkers.plot(title="planeswalkers", kind="bar", ax=ax1)
    ax1.legend(bbox_to_anchor=(1.1, 1))
    ax2.legend(bbox_to_anchor=(1.1, 1))
    ax3.legend(bbox_to_anchor=(1.1, 1))
    ax4.legend(bbox_to_anchor=(1.1, 1))
    ax5.legend(bbox_to_anchor=(1.1, 1))
    ax6.legend(bbox_to_anchor=(1.1, 1))
    plt.subplots_adjust(hspace=0.4, wspace=1.5)
