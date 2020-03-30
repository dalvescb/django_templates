from done import models

def populate():
    # Populate PCBrand Table
    nvidia = models.PCBrand.objects.create(brand_name="Nvidia")
    corsair = models.PCBrand.objects.create(brand_name="Corsair")
    cooler = models.PCBrand.objects.create(brand_name="CoolerMaster")
    msi = models.PCBrand.objects.create(brand_name="MSI")
    intel = models.PCBrand.objects.create(brand_name="Intel")
    amd = models.PCBrand.objects.create(brand_name="AMD")

    # Populate PCPart Table
    i9 = models.PCPart.objects.create(part_type='CPU',name="i9 9900k")
    i9.brand.add(intel)
    i9.save()
    ryzen = models.PCPart.objects.create(part_type='CPU',name="Ryzen 5 3600x")
    ryzen.brand.add(amd)
    ryzen.save()
    vengence = models.PCPart.objects.create(part_type='RAM',name="Vengence")
    vengence.brand.add(corsair)
    vengence.save()
    ultracool = models.PCPart.objects.create(part_type='CL',name="UltraCool")
    ultracool.brand.add(cooler)
    ultracool.save()
    b450 = models.PCPart.objects.create(part_type='MB',name="Tomohawk B450")
    b450.brand.add(msi)
    b450.save()
    g2080 = models.PCPart.objects.create(part_type='GPU',name="2080ti")
    g2080.brand.add(nvidia,msi)
    g2080.save()
    g2070 = models.PCPart.objects.create(part_type='GPU',name="2070")
    g2070.brand.add(nvidia,msi)
    g2070.save()
