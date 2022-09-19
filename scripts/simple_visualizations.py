import pandas as pd

pd.plotting.register_matplotlib_converters()
import matplotlib.pyplot as plt
import seaborn as sns


def get_collection(data):
    output = {}
    for d in data:
        if d == 0:
            continue
        if d in output.keys():
            output[d] += 1
        else:
            output[d] = 1
    return [output]


plt.style.use("bmh")
standard = pd.read_csv(
    "/mnt/c/Users/JAIME/Desktop/code/mtg_data_miner/scripts/standard.csv",
    index_col="name",
    parse_dates=True,
).fillna(0)

standard_rarity = standard[["rare", "common", "uncommon", "mythic", "format"]].head(15)
fig = plt.figure(figsize=(10, 10))
ax1 = fig.add_subplot(221)
plt.subplots_adjust(hspace=1)

standard_rarity.plot(
    title="standard", kind="bar", xlabel="deck_name", ylabel="cuantity", ax=ax1
)

ax1.get_legend().remove()
standard_rarity.plot(
    title="standard", kind="bar", xlabel="deck_name", ylabel="cuantity"
)
fig.legend(["rare", "comm", "unc", "mythic"])
fig.savefig("rarity.jpg")

standard_collection = standard[[c for c in standard.columns if "domain_" in c]]

standard_d_collection = pd.DataFrame(
    get_collection(standard_collection["domain_collection"])
)
fig = plt.figure(figsize=(10, 10))
ax1 = fig.add_subplot(221)

standard_d_collection.plot(title="standard", ylabel="cuantity", kind="bar", ax=ax1)

fig.legend(bbox_to_anchor=(2, 2))
fig.savefig("collection.jpg")


standard_domain = pd.DataFrame(get_collection(standard_collection["domain_collection"]))
standard_lands = pd.DataFrame(
    get_collection(standard_collection["lands_domain_collection"])
)
standard_spells = pd.DataFrame(
    get_collection(standard_collection["spells_domain_collection"])
)
standard_artifacts = pd.DataFrame(
    get_collection(standard_collection["artifacts_domain_collection"])
)
standard_enchantments = pd.DataFrame(
    get_collection(standard_collection["enchantments_domain_collection"])
)
standard_creatures = pd.DataFrame(
    get_collection(standard_collection["creatures_domain_collection"])
)
standard_planeswalkers = pd.DataFrame(
    get_collection(standard_collection["planeswalkers_domain_collection"])
)
fig = plt.figure(figsize=(15, 15))
ax1 = fig.add_subplot(331)
ax2 = fig.add_subplot(332)
ax3 = fig.add_subplot(333)
ax4 = fig.add_subplot(334)
ax5 = fig.add_subplot(335)
ax6 = fig.add_subplot(336)
standard_lands.plot(title="lands", kind="bar", ax=ax2)
standard_spells.plot(title="spells", kind="bar", ax=ax3)
standard_artifacts.plot(title="artifacts", kind="bar", ax=ax4)
standard_enchantments.plot(title="enchantments", kind="bar", ax=ax5)
standard_creatures.plot(title="creatures", kind="bar", ax=ax6)
standard_planeswalkers.plot(title="planeswalkers", kind="bar", ax=ax1)
ax1.legend(bbox_to_anchor=(1.1, 1))
ax2.legend(bbox_to_anchor=(1.1, 1))
ax3.legend(bbox_to_anchor=(1.1, 1))
ax4.legend(bbox_to_anchor=(1.1, 1))
ax5.legend(bbox_to_anchor=(1.1, 1))
ax6.legend(bbox_to_anchor=(1.1, 1))
plt.subplots_adjust(hspace=0.4, wspace=1.5)
fig.savefig("collection_by_type.jpg")
