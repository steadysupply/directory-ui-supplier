from django import forms

sector_choice_value_seo_pairs = [
    ('AEROSPACE', 'aerospace'),
    ('AGRICULTURE_HORTICULTURE_AND_FISHERIES',
        'agriculture-horticulture-and-fisheries'),
    ('AIRPORTS', 'airports'),
    ('AUTOMOTIVE', 'automotive'),
    ('BIOTECHNOLOGY_AND_PHARMACEUTICALS', 'biotechnology-and-pharmaceuticals'),
    ('BUSINESS_AND_CONSUMER_SERVICES', 'business-and-consumer-services'),
    ('CHEMICALS', 'chemicals'),
    ('CLOTHING_FOOTWEAR_AND_FASHION', 'clothing-footwear-and-fashion'),
    ('COMMUNICATIONS', 'communications'),
    ('CONSTRUCTION', 'construction'),
    ('CREATIVE_AND_MEDIA', 'creative-and-media'),
    ('EDUCATION_AND_TRAINING', 'education-and-training'),
    ('ELECTRONICS_AND_IT_HARDWARE', 'electronics-and-it-hardware'),
    ('ENVIRONMENT', 'environment'),
    ('FINANCIAL_AND_PROFESSIONAL_SERVICES',
        'financial-and-professional-services'),
    ('FOOD_AND_DRINK', 'food-and-drink'),
    ('GIFTWARE_JEWELLERY_AND_TABLEWARE', 'giftware-jewellery-and-tableware'),
    ('GLOBAL_SPORTS_INFRASTRUCTURE', 'global-sports-infrastructure'),
    ('HEALTHCARE_AND_MEDICAL', 'healthcare-and-medical'),
    ('HOUSEHOLD_GOODS_FURNITURE_AND_FURNISHINGS',
        'household-goods-furniture-and-furnishings'),
    ('LEISURE_AND_TOURISM', 'leisure-and-tourism'),
    ('MARINE', 'marine'),
    ('MECHANICAL_ELECTRICAL_AND_PROCESS_ENGINEERING',
        'mechanical-electrical-and-process-engineering'),
    ('METALLURGICAL_PROCESS_PLANT', 'metallurgical-process-plant'),
    ('METALS_MINERALS_AND_MATERIALS', 'metals-minerals-and-materials'),
    ('MINING', 'mining'),
    ('OIL_AND_GAS', 'oil-and-gas'),
    ('PORTS_AND_LOGISTICS', 'ports-and-logistics'),
    ('POWER', 'power'),
    ('RAILWAYS', 'railways'),
    ('RENEWABLE_ENERGY', 'renewable-energy'),
    ('RETAIL_AND_LUXURY', 'retail-and-luxury'),
    ('SECURITY', 'security'),
    ('SOFTWARE_AND_COMPUTER_SERVICES', 'software-and-computer-services'),
    ('TEXTILES_INTERIOR_TEXTILES_AND_CARPETS',
        'textiles-interior-textiles-and-carpets'),
    ('WATER', 'water'),
]


class SeoFriendlyChoiceField(forms.ChoiceField):
    """
    The field value is exposed in the URL when then form is submitted.
    `sector=FOOD_AND_DRINK`, for example, would not look great visually, and
    there are SEO implications. Functionality added to this field allows the
    url to show `food-and-drink`, and it will be converted to `FOOD_AND_DRINK`

    """

    choice_values_to_seo_friendly_sectors = {
        choice: seo for choice, seo in sector_choice_value_seo_pairs
    }
    seo_friendly_sectors_to_choice_values = {
        seo: choice for choice, seo in sector_choice_value_seo_pairs
    }

    def to_seo_friendly(self, value):
        return self.choice_values_to_seo_friendly_sectors[value]

    def to_choice_value(self, value):
        return self.seo_friendly_sectors_to_choice_values[value]

    def __init__(self, *, choices=(), **kwargs):
        choices = [
            (self.to_seo_friendly(value), label) for value, label in choices
        ]
        super().__init__(choices=choices, **kwargs)

    def clean(self, value):
        value = super().clean(value)
        return self.to_choice_value(value)
